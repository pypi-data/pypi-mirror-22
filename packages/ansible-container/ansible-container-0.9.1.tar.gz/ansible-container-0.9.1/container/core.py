# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from .utils.visibility import getLogger
logger = getLogger(__name__)

import logging
plainLogger = logging.getLogger(__name__)

import getpass
import gzip
import hashlib
import io
import os
import re
import ruamel
import shutil
import sys
import subprocess
import tarfile
import time
import tempfile

try:
    from shlex import quote
except ImportError:
    from pipes import quote

import requests
from six.moves.urllib.parse import urljoin

from .exceptions import AnsibleContainerAlreadyInitializedException,\
                        AnsibleContainerRegistryAttributeException, \
                        AnsibleContainerException
from .utils import *
from . import __version__, host_only, conductor_only, ENV
from container.utils.loader import load_engine

if ENV == 'conductor':
    from container.utils.galaxy import AnsibleContainerGalaxy


REMOVE_HTTP = re.compile('^https?://')
DEFAULT_CONDUCTOR_BASE = 'centos:7'


@host_only
def hostcmd_init(base_path, project=None, **kwargs):
    if project:
        force = kwargs.pop('force')
        if os.listdir(base_path) and not force:
            raise AnsibleContainerAlreadyInitializedException(
                u'The init command can only be run in an empty directory.')
        try:
            namespace, name = project.split('.', 1)
        except ValueError:
            raise ValueError(u'Invalid project name: %r; use '
                             u'"username.project" style syntax.' % project)
        galaxy_base_url = kwargs.pop('server')
        response = requests.get(urljoin(galaxy_base_url, '/api/v1/roles/'),
                                params={'role_type': 'APP',
                                        'namespace': namespace,
                                        'name': name},
                                headers={'Accepts': 'application/json'})
        try:
            response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(u'Could not find %r on Galaxy '
                                            u'server %r: %r' % (project,
                                                                galaxy_base_url,
                                                                e))
        if not response.json()['count']:
            raise ValueError(u'Could not find %r on Galaxy '
                             u'server %r: No such container app' % (project,
                                                                    galaxy_base_url))
        container_app_data = response.json()['results'][0]
        if not all([container_app_data[k] for k in ['github_user',
                                                    'github_repo']]):
            raise ValueError(u'Container app %r does not have a GitHub URL' % project)
        archive_url = u'https://github.com/%s/%s/archive/%s.tar.gz' % (
            container_app_data['github_user'],
            container_app_data['github_repo'],
            container_app_data['github_branch'] or u'master'
        )
        archive = requests.get(archive_url)
        try:
            archive.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(u'Could not get archive at '
                                            u'%r: %r' % (archive_url, e))
        faux_file = io.BytesIO(archive.content)
        gz_obj = gzip.GzipFile(fileobj=faux_file)
        tar_obj = tarfile.TarFile(fileobj=gz_obj)
        members = tar_obj.getmembers()
        # now we do the actual extraction to the path
        for member in members:
            # we only extract files, and remove any relative path
            # bits that might be in the file for security purposes
            # and drop the leading directory, as mentioned above
            if member.isreg() or member.issym():
                parts = member.name.split(os.sep)[1:]
                final_parts = []
                for part in parts:
                    if part != '..' and '~' not in part and '$' not in part:
                        final_parts.append(part)
                member.name = os.path.join(*final_parts)
                tar_obj.extract(member, base_path)
        logger.info(u'Ansible Container initialized from Galaxy container app %r', project)
    else:
        container_cfg = os.path.join(base_path, 'container.yml')
        if os.path.exists(container_cfg):
            raise AnsibleContainerAlreadyInitializedException()
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        template_dir = os.path.join(jinja_template_path(), 'init')
        context = {
            u'ansible_container_version': __version__,
            u'project_name': kwargs.get('project_name',
                                        os.path.basename(base_path)),
            u'default_base': DEFAULT_CONDUCTOR_BASE
        }
        for tmpl_filename in os.listdir(template_dir):
            jinja_render_to_temp(template_dir,
                                 tmpl_filename,
                                 base_path,
                                 tmpl_filename.replace('.j2', ''),
                                 **context)
        logger.info('Ansible Container initialized.')


@host_only
def hostcmd_build(base_path, project_name, engine_name, var_file=None,
                 **kwargs):
    config = get_config(base_path, var_file=var_file, engine_name=engine_name)
    engine_obj = load_engine(['BUILD', 'RUN'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)

    conductor_container_id = engine_obj.get_container_id_for_service('conductor')
    conductor_image_id = engine_obj.get_latest_image_id_for_service('conductor')
    if engine_obj.service_is_running('conductor'):
        engine_obj.stop_container(conductor_container_id, forcefully=True)

    if conductor_image_id is None or not kwargs.get('devel'):
        #TODO once we get a conductor running, figure out how to know it's running
        if engine_obj.CAP_BUILD_CONDUCTOR:
            engine_obj.build_conductor_image(
                base_path,
                config.get('settings', {}).get('conductor_base', DEFAULT_CONDUCTOR_BASE),
                cache=kwargs['cache']
            )
        else:
            logger.warning(u'%s does not support building the Conductor image.',
                           engine_obj.display_name, engine=engine_obj.display_name)

    if conductor_container_id:
        engine_obj.delete_container(conductor_container_id)

    logger.debug('Config settings', config=config, rawsettings=config.get('settings'),
                 tconf=type(config), settings=config.get('settings', {}))
    save_container = config.get('settings', {}).get('save_conductor_container', False)
    if kwargs.get('save_conductor_container'):
        # give precedence to CLI option
        save_container = True
    engine_obj.await_conductor_command(
        'build', dict(config), base_path, kwargs, save_container=save_container)

@host_only
def hostcmd_deploy(base_path, project_name, engine_name, var_file=None,
                   cache=True, **kwargs):
    assert_initialized(base_path)
    logger.debug('Got extra args to `deploy` command', arguments=kwargs)
    config = get_config(base_path, var_file=var_file, engine_name=engine_name)
    local_images = kwargs.get('local_images')
    output_path = kwargs.pop('deployment_output_path', None) or config.deployment_path

    engine_obj = load_engine(['LOGIN', 'PUSH', 'DEPLOY'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)

    params = {
        'deployment_output_path': os.path.normpath(os.path.expanduser(output_path)),
        'host_user_uid': os.getuid(),
        'host_user_gid': os.getgid(),
    }
    if config.get('settings', {}).get('k8s_auth'):
        params['k8s_auth'] = config['settings']['k8s_auth']
    if kwargs:
        params.update(kwargs)

    if not local_images:
        url, namespace = push_images(base_path, engine_obj, config, save_conductor=False, **params)
        params['url'] = url
        params['namespace'] = namespace

    engine_obj.await_conductor_command(
        'deploy', dict(config), base_path, params,
        save_container=config.get('settings', {}).get('save_conductor_container', False))

@host_only
def hostcmd_run(base_path, project_name, engine_name, var_file=None, cache=True,
                **kwargs):
    assert_initialized(base_path)
    logger.debug('Got extra args to `run` command', arguments=kwargs)
    config = get_config(base_path, var_file=var_file, engine_name=engine_name)
    if not kwargs['production']:
        config.set_env('dev')

    logger.debug('hostcmd_run configuration', config=config.__dict__)

    engine_obj = load_engine(['RUN'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)

    remove_existing_container(engine_obj, 'conductor', remove_volumes=True)

    params = {
        'deployment_output_path': config.deployment_path,
        'host_user_uid': os.getuid(),
        'host_user_gid': os.getgid(),
    }
    if config.get('settings', {}).get('k8s_auth'):
        params['k8s_auth'] = config['settings']['k8s_auth']
    if kwargs:
        params.update(kwargs)

    logger.debug('Params passed to conductor for run', params=params)

    engine_obj.await_conductor_command(
        'run', dict(config), base_path, params,
        save_container=config.get('settings', {}).get('save_conductor_container', False))

@host_only
def hostcmd_destroy(base_path, project_name, engine_name, var_file=None, cache=True,
                  **kwargs):
    assert_initialized(base_path)
    logger.debug('Got extra args to `destroy` command', arguments=kwargs)
    config = get_config(base_path, var_file=var_file, engine_name=engine_name)

    engine_obj = load_engine(['RUN'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)

    remove_existing_container(engine_obj, 'conductor', remove_volumes=True)

    params = {
        'deployment_output_path': config.deployment_path,
        'host_user_uid': os.getuid(),
        'host_user_gid': os.getgid(),
    }
    if config.get('settings', {}).get('k8s_auth'):
        params['k8s_auth'] = config['settings']['k8s_auth']
    if kwargs:
        params.update(kwargs)
    params.update(kwargs)

    engine_obj.await_conductor_command(
        'destroy', dict(config), base_path, params,
        save_container=config.get('settings', {}).get('save_conductor_container', False))

@host_only
def hostcmd_stop(base_path, project_name, engine_name, force=False, services=[],
                 **kwargs):
    config = get_config(base_path, engine_name=engine_name)
    engine_obj = load_engine(['RUN'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)

    params = {
        'deployment_output_path': config.deployment_path,
        'host_user_uid': os.getuid(),
        'host_user_gid': os.getgid(),
    }
    if config.get('settings', {}).get('k8s_auth'):
        params['k8s_auth'] = config['settings']['k8s_auth']
    if kwargs:
        params.update(kwargs)
    params.update(kwargs)

    engine_obj.await_conductor_command(
        'stop', dict(config), base_path, params,
        save_container=config.get('settings', {}).get('save_conductor_container', False))


@host_only
def hostcmd_restart(base_path, project_name, engine_name, force=False, services=[],
                    **kwargs):
    config = get_config(base_path, engine_name=engine_name)
    engine_obj = load_engine(['RUN'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)
    params = {
        'deployment_output_path': config.deployment_path,
        'host_user_uid': os.getuid(),
        'host_user_gid': os.getgid(),
    }
    if config.get('settings', {}).get('k8s_auth'):
        params['k8s_auth'] = config['settings']['k8s_auth']
    if kwargs:
        params.update(kwargs)
    params.update(kwargs)

    engine_obj.await_conductor_command(
        'restart', dict(config), base_path, params,
        save_container=config.get('settings', {}).get('save_conductor_container', False))


@host_only
def hostcmd_push(base_path, project_name, engine_name, var_file=None, **kwargs):
    """
    Push images to a registry. Requires authenticating with the registry prior to starting
    the push. If your engine's config file does not already contain an authorization for the
    registry, pass username and/or password. If you exclude password, you will be prompted.
    """
    assert_initialized(base_path)
    config = get_config(base_path, var_file=var_file, engine_name=engine_name)

    engine_obj = load_engine(['LOGIN', 'PUSH'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)
    push_images(base_path,
                engine_obj,
                config,
                save_conductor=config.get('settings', {}).get('save_conductor_container', False),
                **kwargs)


@host_only
def push_images(base_path, engine_obj, config, **kwargs):
    """ Pushes images to a Docker registry. Returns (url, namespace) used to push images. """
    config_path = kwargs.get('config_path', engine_obj.auth_config_path)
    username = kwargs.get('username')
    password = kwargs.get('password')
    push_to = kwargs.get('push_to')
    url = engine_obj.default_registry_url
    registry_name = engine_obj.default_registry_name
    namespace = None
    save_conductor = config.get('settings', {}).get('save_conductor_container', False)

    if push_to:
        if config.get('registries', dict()).get(push_to):
            url = config['registries'][push_to].get('url')
            namespace = config['registries'][push_to].get('namespace')
            if not url:
                raise AnsibleContainerRegistryAttributeException(
                    u"Registry {} missing required attribute 'url'".format(push_to)
                )
        else:
            url, namespace = resolve_push_to(push_to, engine_obj.default_registry_url)

    if username and not password:
        # If a username was supplied without a password, prompt for it
        while not password:
            password = getpass.getpass(u"Enter password for {0} at {1}: ".format(username, registry_name))

    if config_path:
        # Make sure the config_path exists
        #  - gives us a chance to create the file with correct permissions, if it does not exists
        #  - makes sure we mount a path to the conductor for a specific file
        config_path = os.path.normpath(os.path.expanduser(config_path))
        if os.path.exists(config_path) and os.path.isdir(config_path):
            raise AnsibleContainerException(
                u"Expecting --config-path to be a path to a file and not a directory"
            )
        elif not os.path.exists(config_path):
            # Make sure the directory path exists
            try:
                os.makedirs(os.path.dirname(config_path), 0o750)
            except OSError:
                raise AnsibleContainerException(
                    u"Failed to create the requested the path {}".format(os.path.dirname(config_path))
                )
            # Touch the file
            open(config_path, 'w').close()

    # If you ran build with --save-build-container, then you're broken without first removing
    #  the old build container.
    remove_existing_container(engine_obj, 'conductor', remove_volumes=True)

    push_params = {}
    push_params.update(kwargs)
    push_params['config_path'] = config_path
    push_params['password'] = password
    push_params['url'] = url
    push_params['namespace'] = namespace
    engine_obj.await_conductor_command('push', dict(config), base_path, push_params, save_container=save_conductor)
    return url, namespace


@host_only
def hostcmd_install(base_path, project_name, engine_name, **kwargs):
    assert_initialized(base_path)
    config = get_config(base_path, engine_name=engine_name)
    save_conductor = config.get('settings', {}).get('save_conductor_container', False)
    engine_obj = load_engine(['INSTALL'],
                             engine_name, project_name or os.path.basename(base_path),
                             config['services'], **kwargs)
    engine_obj.await_conductor_command('install',
                                       dict(config),
                                       base_path,
                                       kwargs,
                                       save_container=save_conductor)

@host_only
def hostcmd_version(base_path, project_name, engine_name, **kwargs):
    print('Ansible Container, version', __version__)
    if kwargs.get('debug', False):
        print(u', '.join(os.uname()))
        print(sys.version, sys.executable)
        assert_initialized(base_path)
        engine_obj = load_engine(['VERSION'],
                                 engine_name,
                                 project_name or os.path.basename(base_path),
                                 {}, **kwargs)
        engine_obj.print_version_info()


@host_only
def hostcmd_import(base_path, project_name, engine_name, **kwargs):
    engine_obj = load_engine(['IMPORT'],
                             engine_name,
                             project_name or os.path.basename(base_path),
                             {}, **kwargs)

    engine_obj.import_project(base_path, **kwargs)
    logger.info('Project imported.')


@host_only
def remove_existing_container(engine_obj, service_name, remove_volumes=False):
    """
    Remove a container for an existing service. Handy for removing an existing conductor.
    """
    conductor_container_id = engine_obj.get_container_id_for_service(service_name)
    if engine_obj.service_is_running(service_name):
        engine_obj.stop_container(conductor_container_id, forcefully=True)
    if conductor_container_id:
        engine_obj.delete_container(conductor_container_id, remove_volumes=remove_volumes)


@host_only
def resolve_push_to(push_to, default_url):
    '''
    Given a push-to value, return the registry and namespace.

    :param push_to: string: User supplied --push-to value.
    :param default_url: string: Container engine's default_index value (e.g. docker.io).
    :return: tuple: registry_url, namespace
    '''
    protocol = 'http://' if push_to.startswith('http://') else 'https://'
    url = push_to = REMOVE_HTTP.sub('', push_to)
    namespace = None
    parts = url.split('/', 1)
    special_set = {'.', ':'}
    char_set = set([c for c in parts[0]])

    if len(parts) == 1:
        if not special_set.intersection(char_set) and parts[0] != 'localhost':
            registry_url = default_url
            namespace = push_to
        else:
            registry_url = protocol + parts[0]
    else:
        registry_url = protocol + parts[0]
        namespace = parts[1]

    return registry_url, namespace


@conductor_only
def run_playbook(playbook, engine, service_map, ansible_options='', local_python=False, debug=False,
                 deployment_output_path=None, tags=None, **kwargs):
    uid, gid = kwargs.get('host_user_uid', 1), kwargs.get('host_user_gid', 1)

    try:
        if deployment_output_path:
            remove_tmpdir = False
            output_dir = deployment_output_path
        else:
            remove_tmpdir = True
            output_dir = tempfile.mkdtemp()

        os.chown(output_dir, uid, gid)

        playbook_path = os.path.join(output_dir, 'playbook.yml')
        logger.debug("writing playbook to {}".format(playbook_path))
        logger.debug("playbook", playbook=playbook)
        with open(playbook_path, 'w') as ofs:
            ofs.write(ruamel.yaml.round_trip_dump(playbook, indent=4, block_seq_indent=2, default_flow_style=False))

        inventory_path = os.path.join(output_dir, 'hosts')
        with open(inventory_path, 'w') as ofs:
            for service_name, container_id in service_map.items():
                if not local_python:
                    # Use Python runtime from conductor
                    ofs.write('%s ansible_host="%s" ansible_python_interpreter="%s"\n' % (
                        service_name, container_id, engine.python_interpreter_path))
                else:
                    # Use local Python runtime
                    ofs.write('%s ansible_host="%s"\n' % (service_name, container_id))


        if not os.path.exists(os.path.join(output_dir, 'files')):
            os.mkdir(os.path.join(output_dir, 'files'))
        if not os.path.exists(os.path.join(output_dir, 'templates')):
            os.mkdir(os.path.join(output_dir, 'templates'))

        for root, dirs, files in os.walk(output_dir):
            for d in dirs:
                logger.debug('found dir %s', os.path.join(root, d))
                os.chown(os.path.join(root, d), uid, gid)
            for f in files:
                logger.debug('found file %s', os.path.join(root, f))
                os.chown(os.path.join(root, f), uid, gid)


        rc = subprocess.call(['mount', '--bind', '/src',
                              os.path.join(output_dir, 'files')])
        if rc:
            raise OSError('Could not bind-mount /src into tmpdir')
        rc = subprocess.call(['mount', '--bind', '/src',
                              os.path.join(output_dir, 'templates')])
        if rc:
            raise OSError('Could not bind-mount /src into tmpdir')

        ansible_args = dict(inventory=quote(inventory_path),
                            playbook=quote(playbook_path),
                            debug_maybe='-vvvv' if debug else '',
                            engine_args=engine.ansible_args,
                            ansible_playbook=engine.ansible_exec_path,
                            ansible_options=' '.join(ansible_options) or '')
        if tags:
            ansible_args['ansible_options'] += ' --tags={} '.format(','.join(tags))
        else:
            pass
        # env = os.environ.copy()
        # env['ANSIBLE_REMOTE_TEMP'] = '/tmp/.ansible-${USER}/tmp'

        ansible_cmd = ('{ansible_playbook} '
                       '{debug_maybe} '
                       '{ansible_options} '
                       '-i {inventory} '
                       '{engine_args} '
                       '{playbook}').format(**ansible_args)
        logger.debug('Running Ansible Playbook', command=ansible_cmd, cwd='/src')
        process = subprocess.Popen(ansible_cmd,
                                   shell=True,
                                   bufsize=1,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   cwd='/src',
                                   #env=env
                                   )

        log_iter = iter(process.stdout.readline, '')
        while process.returncode is None:
            try:
                plainLogger.info(log_iter.next().rstrip())
            except StopIteration:
                process.wait()
            finally:
                process.poll()

        return process.returncode
    finally:
        try:
            rc = subprocess.call(['unmount',
                                  os.path.join(output_dir, 'files')])
            rc = subprocess.call(['unmount',
                                  os.path.join(output_dir, 'templates')])
        except Exception:
            pass
        try:
            if remove_tmpdir:
                shutil.rmtree(output_dir, ignore_errors=True)
        except Exception:
            pass


@conductor_only
def apply_role_to_container(role, container_id, service_name, engine, vars={},
                            local_python=False, ansible_options='',
                            debug=False):
    playbook = [
        {'hosts': service_name,
         'vars': vars,
         'roles': [role],
         }
    ]

    if isinstance(role, dict) and 'gather_facts' in role:
        # Allow disabling gather_facts at the role level
        playbook[0]['gather_facts'] = role.pop('gather_facts')

    container_metadata = engine.inspect_container(container_id)
    onbuild = container_metadata['Config']['OnBuild']
    # FIXME: Actually do stuff if onbuild is not null

    rc = run_playbook(playbook, engine, {service_name: container_id}, ansible_options=ansible_options,
                      local_python=local_python, debug=debug)
    if rc:
        logger.error('Error applying role!', playbook=playbook, engine=engine,
            exit_code=rc)
    return rc


@conductor_only
def conductorcmd_build(engine_name, project_name, services, cache=True,
                       local_python=False, ansible_options='', debug=False, **kwargs):
    engine = load_engine(['BUILD'], engine_name, project_name, services, **kwargs)
    logger.info(u'%s integration engine loaded. Build starting.',
        engine.display_name, project=project_name)
    services_to_build = kwargs.get('services_to_build') or services.keys()
    for service_name, service in services.items():
        if service_name not in services_to_build:
            logger.debug('Skipping service %s...', service_name)
            continue
        logger.info(u'Building service...', service=service_name, project=project_name)
        cur_image_id = engine.get_image_id_by_tag(service['from'])
        # the fingerprint hash tracks cacheability
        fingerprint_hash = hashlib.sha256('%s::' % cur_image_id)
        logger.debug(u'Base fingerprint hash = %s', fingerprint_hash.hexdigest(),
                     service=service_name, hash=fingerprint_hash.hexdigest())
        cache_busted = not cache

        cur_container_id = engine.get_container_id_for_service(service_name)
        if cur_container_id:
            if engine.service_is_running(service_name):
                engine.stop_container(cur_container_id, forcefully=True)
            engine.delete_container(cur_container_id)

        if service.get('roles'):
            for role in service['roles']:
                role_fingerprint = get_role_fingerprint(role)
                fingerprint_hash.update(role_fingerprint)

                if not cache_busted:
                    logger.debug(u'Still trying to keep cache.', service=service_name)
                    cached_image_id = engine.get_image_id_by_fingerprint(
                        fingerprint_hash.hexdigest())
                    if cached_image_id:
                        # We can reuse the cached image
                        logger.debug(u'Cached layer found for service',
                                     service=service_name, fingerprint=fingerprint_hash.hexdigest())
                        cur_image_id = cached_image_id
                        logger.info(u'Applied role %s from cache', role,
                                    service=service_name, role=role)
                        continue
                    else:
                        cache_busted = True
                        logger.debug(u'Cache busted! No layer found',
                            service=service_name,
                            fingerprint=fingerprint_hash.hexdigest(),
                        )
                run_kwargs = dict(
                    name=engine.container_name_for_service(service_name),
                    user='root',
                    working_dir='/',
                    command='sh -c "while true; do sleep 1; '
                            'done"',
                    entrypoint=[],
                    privileged=True,
                    volumes=dict()
                )

                if service.get('volumes'):
                    for volume in service['volumes']:
                        pieces = volume.split(':')
                        src = pieces[0]
                        bind = pieces[0]
                        mode = 'rw'
                        if len(pieces) > 1:
                            bind = pieces[1]
                        if len(pieces) > 2:
                            mode = pieces[2]
                        run_kwargs[u'volumes'][src] = {u'bind': bind, u'mode': mode}

                if not local_python:
                    # If we're on a debian based distro, we need the correct architecture
                    # to allow python to load dynamically loaded shared libraries
                    extra_library_paths = ''
                    try:
                        architecture = subprocess.check_output(['dpkg-architecture',
                                                                   '-qDEB_HOST_MULTIARCH'])
                        architecture = architecture.strip()
                        logger.debug(u'Detected architecture %s', architecture,
                                       service=service_name, architecture=architecture)
                        extra_library_paths = (':/_usr/lib/{0}:/_usr/local/lib/{0}'
                                               ':/_lib/{0}').format(architecture)
                    except Exception:
                        # we're not on debian/ubuntu or a system without multiarch support
                        pass

                    # Use the conductor's Python runtime
                    run_kwargs['volumes'] = {engine.get_runtime_volume_id('/usr'): {'bind': '/_usr', 'mode': 'ro'}}
                    try:
                        run_kwargs['volumes'][engine.get_runtime_volume_id('/lib')] = {'bind': '/_lib', 'mode': 'ro'}
                        extra_library_paths += ":/_lib"
                    except ValueError:
                        # No /lib volume
                        pass
                    run_kwargs['environment'] = dict(
                         LD_LIBRARY_PATH='/_usr/lib:/_usr/lib64:/_usr/local/lib{}'.format(extra_library_paths),
                         CPATH='/_usr/include:/_usr/local/include',
                         PATH='/usr/local/sbin:/usr/local/bin:'
                              '/usr/sbin:/usr/bin:/sbin:/bin:'
                              '/_usr/sbin:/_usr/bin:'
                              '/_usr/local/sbin:/_usr/local/bin',
                         PYTHONPATH='/_usr/lib/python2.7')

                container_id = engine.run_container(cur_image_id, service_name, **run_kwargs)

                while not engine.service_is_running(service_name):
                    time.sleep(0.2)
                logger.debug('Container running', id=container_id)

                rc = apply_role_to_container(role, container_id, service_name,
                                             engine, vars=dict(service['defaults']),
                                             local_python=local_python,
                                             ansible_options=ansible_options,
                                             debug=debug)
                logger.debug('Playbook run finished.', exit_code=rc)
                if rc:
                    raise RuntimeError('Build failed.')
                logger.info(u'Applied role to service', service=service_name, role=role)

                engine.stop_container(container_id, forcefully=True)
                is_last_role = role is service['roles'][-1]
                if is_last_role and kwargs.get('flatten'):
                    logger.debug("Finished build, flattening image")
                    image_id = engine.flatten_container(container_id, service_name, service)
                    logger.info(u'Saved flattened image for service', service=service_name, image=image_id)
                else:
                    image_id = engine.commit_role_as_layer(container_id,
                                                           service_name,
                                                           fingerprint_hash.hexdigest(),
                                                           service,
                                                           with_name=is_last_role)
                    logger.info(u'Committed layer as image', service=service_name, image=image_id)
                engine.delete_container(container_id)
                cur_image_id = image_id
            # Tag the image also as latest:
            engine.tag_image_as_latest(service_name, cur_image_id)
            logger.info(u'Build complete.', service=service_name)
        else:
            logger.info(u'Service had no roles specified. Nothing to do.', service=service_name)
    logger.info(u'All images successfully built.')


@conductor_only
def conductorcmd_run(engine_name, project_name, services, **kwargs):
    engine = load_engine(['RUN'], engine_name, project_name, services, **kwargs)

    logger.info(u'Engine integration loaded. Preparing run.',
                engine=engine.display_name)

    engine.containers_built_for_services(
        [service for service, service_desc in services.items()
         if service_desc.get('roles')])

    logger.debug("In conductorcmd_run", kwargs=kwargs)
    playbook = engine.generate_orchestration_playbook(**kwargs)
    logger.debug("in conductorcmd_run", playbook=playbook)
    rc = run_playbook(playbook, engine, services, tags=['start'], **kwargs)
    logger.info(u'All services running.', playbook_rc=rc)


@conductor_only
def conductorcmd_restart(engine_name, project_name, services, **kwargs):
    engine = load_engine(['RUN'], engine_name, project_name, services, **kwargs)
    logger.info(u'Engine integration loaded. Preparing to restart containers.',
                engine=engine.display_name)
    playbook = engine.generate_orchestration_playbook(**kwargs)
    rc = run_playbook(playbook, engine, services, tags=['restart'], **kwargs)
    logger.info(u'All services restarted.', playbook_rc=rc)


@conductor_only
def conductorcmd_stop(engine_name, project_name, services, **kwargs):
    engine = load_engine(['RUN'], engine_name, project_name, services, **kwargs)
    logger.info(u'Engine integration loaded. Preparing to stop all containers.',
                engine=engine.display_name)
    playbook = engine.generate_orchestration_playbook(**kwargs)
    rc = run_playbook(playbook, engine, services, tags=['stop'], **kwargs)
    logger.info(u'All services stopped.', playbook_rc=rc)


@conductor_only
def conductorcmd_destroy(engine_name, project_name, services, **kwargs):
    engine = load_engine(['RUN'], engine_name, project_name, services, **kwargs)
    logger.info(u'Engine integration loaded. Preparing to stop+delete all '
                u'containers and built images.',
                engine=engine.display_name)
    playbook = engine.generate_orchestration_playbook(**kwargs)
    rc = run_playbook(playbook, engine, services, tags=['destroy'], **kwargs)
    logger.info(u'All services destroyed.', playbook_rc=rc)

@conductor_only
def conductorcmd_deploy(engine_name, project_name, services, **kwargs):
    engine = load_engine(['DEPLOY'], engine_name, project_name, services, **kwargs)
    logger.info(u'Engine integration loaded. Preparing deploy.',
                engine=engine.display_name)

    # Verify all images are built
    for service_name in services:
        if not services[service_name].get('roles'):
            continue
        logger.info(u'Verifying image for %s', service_name)
        image_id = engine.get_latest_image_id_for_service(service_name)
        if not image_id:
            logger.error(u'Missing image. Run "ansible-container build" '
                         u'to (re)create it.', service=service_name)
            raise RuntimeError(u'Run failed.')

    logger.debug("conductorcmd_deploy", kwargs=kwargs)

    deployment_output_path = kwargs.get('deployment_output_path')
    playbook = engine.generate_orchestration_playbook(**kwargs)

    try:
        with open(os.path.join(deployment_output_path, '%s.yml' % project_name), 'w') as ofs:
            ofs.write(ruamel.yaml.round_trip_dump(playbook, indent=4, block_seq_indent=2, default_flow_style=False))

    except OSError:
        logger.error(u'Failure writing deployment playbook', exc_info=True)
        raise


@conductor_only
def conductorcmd_install(engine_name, project_name, services, **kwargs):
    roles = kwargs.pop('roles', None)
    logger.debug("Installing roles", roles=roles)
    if roles:
        galaxy = AnsibleContainerGalaxy()
        galaxy.install(roles)

@conductor_only
def conductorcmd_push(engine_name, project_name, services, **kwargs):
    """ Push images to a registry """
    username = kwargs.pop('username')
    password = kwargs.pop('password')
    email = kwargs.pop('email')
    url = kwargs.pop('url')
    namespace = kwargs.pop('namespace')
    tag = kwargs.pop('tag')
    config_path = kwargs.pop('config_path')

    engine = load_engine(['PUSH', 'LOGIN'], engine_name, project_name, services)
    logger.info(u'Engine integration loaded. Preparing push.',
                engine=engine.display_name)

    # Verify that we can authenticate with the registry
    username, password = engine.login(username, password, email, url, config_path)

    repo_data = {
        'url': url,
        'namespace': namespace or username,
        'tag': tag,
        'username': username,
        'password': password
    }

    # Push each image that has been built using Ansible roles
    for service_name, service_config in services.items():
        if service_config.get('roles'):
            # if the service has roles, it's an image we should push
            image_id = engine.get_latest_image_id_for_service(service_name)
            engine.push(image_id, service_name, repo_data)
