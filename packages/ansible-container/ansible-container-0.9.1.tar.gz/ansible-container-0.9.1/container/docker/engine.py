# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
plainLogger = logging.getLogger(__name__)

from container.utils.visibility import getLogger
logger = getLogger(__name__)

import base64
import datetime
import functools
import time
import inspect
import json
import os
import re
import six
import sys
import tarfile

try:
    import httplib as StatusCodes
except ImportError:
    from http import HTTPStatus as StatusCodes

import container
from container import host_only, conductor_only
from container.engine import BaseEngine
from container import utils, exceptions
from container.utils import logmux, text, ordereddict_to_list

try:
    import docker
    from docker import errors as docker_errors
    from docker.utils.ports import build_port_bindings
    from docker.errors import DockerException
    from docker.api.container import ContainerApiMixin
    from docker.models.containers import RUN_HOST_CONFIG_KWARGS
except ImportError:
    raise ImportError(
        u'You must install Ansible Container with Docker(tm) support. '
        u'Try:\npip install ansible-container==%s[docker]' % (
        container.__version__
    ))

TEMPLATES_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        'templates'))

FILES_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        'files'))

DOCKER_VERSION = '17.04.0-ce'

DOCKER_DEFAULT_CONFIG_PATH = os.path.join(os.environ.get('HOME', ''), '.docker', 'config.json')

DOCKER_CONFIG_FILEPATH_CASCADE = [
    os.environ.get('DOCKER_CONFIG', ''),
    DOCKER_DEFAULT_CONFIG_PATH,
    os.path.join(os.environ.get('HOME', ''), '.dockercfg')
]

REMOVE_HTTP = re.compile('^https?://')


def log_runs(fn):
    @functools.wraps(fn)
    def __wrapped__(self, *args, **kwargs):
        logger.debug(
            u'Call: %s.%s' % (type(self).__name__, fn.__name__),
            # because log_runs is a decorator, we need to override the caller
            # line & function
            caller_func='%s.%s' % (type(self).__name__, fn.__name__),
            caller_line=inspect.getsourcelines(fn)[-1],
            args=args,
            kwargs=kwargs,
        )
        return fn(self, *args, **kwargs)
    return __wrapped__


class Engine(BaseEngine):

    # Capabilities of engine implementations
    CAP_BUILD_CONDUCTOR = True
    CAP_BUILD = True
    CAP_DEPLOY = True
    CAP_IMPORT = True
    CAP_INSTALL = True
    CAP_LOGIN = True
    CAP_PUSH = True
    CAP_RUN = True
    CAP_VERSION = True

    COMPOSE_WHITELIST = (
        'links', 'depends_on', 'cap_add', 'cap_drop', 'command', 'devices',
        'dns', 'dns_opt', 'tmpfs', 'entrypoint', 'environment', 'expose',
        'external_links', 'labels', 'links', 'logging', 'log_opt', 'networks',
        'network_mode', 'pids_limit', 'ports', 'security_opt', 'stop_grace_period',
        'stop_signal', 'sysctls', 'ulimits', 'userns_mode', 'volumes',
        'volume_driver', 'volumes_from', 'cpu_shares', 'cpu_quota', 'cpuset',
        'domainname', 'hostname', 'ipc', 'mac_address', 'mem_limit',
        'memswap_limit', 'mem_swappiness', 'mem_reservation', 'oom_score_adj',
        'privileged', 'read_only', 'restart', 'shm_size', 'stdin_open', 'tty',
        'user', 'working_dir',
    )
    display_name = u'Docker\u2122 daemon'

    _client = None

    FINGERPRINT_LABEL_KEY = 'com.ansible.container.fingerprint'
    LAYER_COMMENT = 'Built with Ansible Container (https://github.com/ansible/ansible-container)'

    @property
    def client(self):
        if not self._client:
            try:
                self._client = docker.from_env(version='auto')
            except DockerException as exc:
                if 'Connection refused' in str(exc):
                    raise exceptions.AnsibleContainerDockerConnectionRefused()
                else:
                    raise
        return self._client

    @property
    def ansible_args(self):
        """Additional commandline arguments necessary for ansible-playbook runs."""
        return u'-c docker'

    @property
    def default_registry_url(self):
        return u'https://index.docker.io/v1/'

    @property
    def default_registry_name(self):
        return u'Docker Hub'

    @property
    def auth_config_path(self):
        result = DOCKER_DEFAULT_CONFIG_PATH
        for path in DOCKER_CONFIG_FILEPATH_CASCADE:
            if path and os.path.exists(path):
                result = os.path.normpath(os.path.expanduser(path))
                break
        return result

    def container_name_for_service(self, service_name):
        return u'%s_%s' % (self.project_name, service_name)

    def image_name_for_service(self, service_name):
        if service_name == 'conductor' or self.services[service_name].get('roles'):
            return u'%s-%s' % (self.project_name.lower(), service_name.lower())
        else:
            return self.services[service_name].get('from')

    def run_kwargs_for_service(self, service_name):
        to_return = self.services[service_name].copy()
        # remove keys that docker-compose format doesn't accept, or that can't
        #  be used during the build phase
        container_args = inspect.getargspec(ContainerApiMixin.create_container)[0] + RUN_HOST_CONFIG_KWARGS
        remove_keys = list(set(to_return.keys()) - set(container_args)) + ['links']
        logger.debug("Removing keys", keys=remove_keys)
        for key in list(remove_keys):
            try:
                to_return.pop(key)
            except KeyError:
                pass
        if to_return.get('ports'):
            # convert ports from a list to a dict that docker-py likes
            new_ports = build_port_bindings(to_return.get('ports'))
            to_return['ports'] = new_ports
        return to_return

    @host_only
    def print_version_info(self):
        print(json.dumps(self.client.info(), indent=2))
        print(json.dumps(self.client.version(), indent=2))

    @log_runs
    @conductor_only
    def run_container(self, image_id, service_name, **kwargs):
        """Run a particular container. The kwargs argument contains individual
        parameter overrides from the service definition."""
        run_kwargs = self.run_kwargs_for_service(service_name)
        run_kwargs.update(kwargs, relax=True)
        logger.debug('Running container in docker', image=image_id, params=run_kwargs)

        container_obj = self.client.containers.run(
            image=image_id,
            detach=True,
            **run_kwargs
        )

        log_iter = container_obj.logs(stdout=True, stderr=True, stream=True)
        mux = logmux.LogMultiplexer()
        mux.add_iterator(log_iter, plainLogger)
        return container_obj.id

    @log_runs
    @host_only
    def run_conductor(self, command, config, base_path, params, engine_name=None, volumes=None):
        image_id = self.get_latest_image_id_for_service('conductor')
        if image_id is None:
            raise exceptions.AnsibleContainerConductorException(
                    u"Conductor container can't be found. Run "
                    u"`ansible-container build` first")

        serialized_params = base64.b64encode(json.dumps(params).encode("utf-8")).decode()
        serialized_config = base64.b64encode(json.dumps(ordereddict_to_list(config)).encode("utf-8")).decode()

        if not volumes:
            volumes = {}

        if params.get('with_volumes'):
            for volume in params.get('with_volumes'):
                volume_parts = volume.split(':')
                volume_parts[0] = os.path.normpath(os.path.abspath(os.path.expanduser(volume_parts[0])))
                volumes[volume_parts[0]] = {
                    'bind': volume_parts[1] if len(volume_parts) > 1 else volume_parts[0],
                    'mode': volume_parts[2] if len(volume_parts) > 2 else 'rw'
                }

        permissions = 'ro' if command != 'install' else 'rw'
        volumes[base_path] = {'bind': '/src', 'mode': permissions}

        if params.get('deployment_output_path'):
            deployment_path = params['deployment_output_path']
            volumes[deployment_path] = {'bind': deployment_path, 'mode': 'rw'}

        roles_path = None
        if params.get('roles_path'):
            # User specified --roles-path
            roles_path = os.path.normpath(os.path.abspath(os.path.expanduser(params.get('roles_path'))))
            volumes[roles_path] = {'bind': roles_path, 'mode': 'ro'}

        environ = {}
        if os.environ.get('DOCKER_HOST'):
            environ['DOCKER_HOST'] = os.environ['DOCKER_HOST']
            if os.environ.get('DOCKER_CERT_PATH'):
                environ['DOCKER_CERT_PATH'] = '/etc/docker'
                volumes[os.environ['DOCKER_CERT_PATH']] = {'bind': '/etc/docker',
                                                           'mode': 'ro'}
            if os.environ.get('DOCKER_TLS_VERIFY'):
                environ['DOCKER_TLS_VERIFY'] = os.environ['DOCKER_TLS_VERIFY']
        else:
            environ['DOCKER_HOST'] = 'unix:///var/run/docker.sock'
            volumes['/var/run/docker.sock'] = {'bind': '/var/run/docker.sock',
                                               'mode': 'rw'}
        if params.get('with_variables'):
            for var in params['with_variables']:
                key, value = var.split('=', 1)
                environ[key] = value

        if roles_path:
            environ['ANSIBLE_ROLES_PATH'] = "%s:/src/roles:/etc/ansible/roles" % roles_path
        else:
            environ['ANSIBLE_ROLES_PATH'] = '/src/roles:/etc/ansible/roles'

        if params.get('devel'):
            conductor_path = os.path.dirname(container.__file__)
            logger.debug(u"Binding Ansible Container code at %s into conductor "
                         u"container", conductor_path)
            volumes[conductor_path] = {'bind': '/_ansible/container', 'mode': 'rw'}

        if command in ('login', 'push') and params.get('config_path'):
            config_path = params.get('config_path')
            volumes[config_path] = {'bind': config_path,
                                    'mode': 'rw'}

        if not engine_name:
            engine_name = __name__.rsplit('.', 2)[-2]

        run_kwargs = dict(
            name=self.container_name_for_service('conductor'),
            command=['conductor',
                     command,
                     '--project-name', self.project_name,
                     '--engine', engine_name,
                     '--params', serialized_params,
                     '--config', serialized_config,
                     '--encoding', 'b64json'],
            detach=True,
            user='root',
            volumes=volumes,
            environment=environ,
            working_dir='/src',
            cap_add=['SYS_ADMIN']
        )

        # Anytime a playbook is executed, /src is bind mounted to a tmpdir, and that seems to
        # require privileged=True
        run_kwargs['privileged'] = True

        logger.debug('Docker run:', image=image_id, params=run_kwargs)
        try:
            container_obj = self.client.containers.run(
                image_id,
                **run_kwargs
            )
        except docker_errors.APIError as exc:
            if exc.response.status_code == StatusCodes.CONFLICT:
                raise exceptions.AnsibleContainerConductorException(
                    u"Can't start conductor container, another conductor for "
                    u"this project already exists or wasn't cleaned up.")
            six.reraise(*sys.exc_info())
        else:
            log_iter = container_obj.logs(stdout=True, stderr=True, stream=True)
            mux = logmux.LogMultiplexer()
            mux.add_iterator(log_iter, plainLogger)
            return container_obj.id

    def await_conductor_command(self, command, config, base_path, params, save_container=False):
        conductor_id = self.run_conductor(command, config, base_path, params)
        try:
            while self.service_is_running('conductor'):
                time.sleep(0.1)
        finally:
            exit_code = self.service_exit_code('conductor')
            msg = 'Preserving as requested.' if save_container else 'Cleaning up.'
            logger.info('Conductor terminated. {}'.format(msg), save_container=save_container,
                        conductor_id=conductor_id, command_rc=exit_code)
            if not save_container:
                self.delete_container(conductor_id, remove_volumes=True)
            if exit_code:
                raise exceptions.AnsibleContainerConductorException(
                    u'Conductor exited with status %s' % exit_code
                )

    def service_is_running(self, service):
        try:
            running_container = self.client.containers.get(self.container_name_for_service(service))
            return running_container.status == 'running' and running_container.id
        except docker_errors.NotFound:
            return False

    def service_exit_code(self, service):
        try:
            container_info = self.client.api.inspect_container(self.container_name_for_service(service))
            return container_info['State']['ExitCode']
        except docker_errors.APIError:
            return None

    def stop_container(self, container_id, forcefully=False):
        try:
            to_stop = self.client.containers.get(container_id)
        except docker_errors.APIError:
            logger.debug(u"Could not find container %s to stop", container_id,
                         id=container_id, force=forcefully)
            pass
        else:
            if forcefully:
                to_stop.kill()
            else:
                to_stop.stop(timeout=60)

    def restart_all_containers(self):
        raise NotImplementedError()

    def inspect_container(self, container_id):
        try:
            return self.client.api.inspect_container(container_id)
        except docker_errors.APIError:
            return None

    def delete_container(self, container_id, remove_volumes=False):
        try:
            to_delete = self.client.containers.get(container_id)
        except docker_errors.APIError:
            pass
        else:
            to_delete.remove(v=remove_volumes)

    def get_container_id_for_service(self, service_name):
        try:
            container_info = self.client.containers.get(self.container_name_for_service(service_name))
        except docker_errors.NotFound:
            logger.debug("Could not find container for %s", service_name,
                         container=self.container_name_for_service(service_name),
                         all_containers=self.client.containers.list())
            return None
        else:
            return container_info.id

    def get_image_id_by_fingerprint(self, fingerprint):
        try:
            image, = self.client.images.list(
                all=True,
                filters=dict(label='%s=%s' % (self.FINGERPRINT_LABEL_KEY,
                                              fingerprint)))
        except ValueError:
            return None
        else:
            return image.id

    def get_image_id_by_tag(self, tag):
        try:
            image = self.client.images.get(tag)
            return image.id
        except docker_errors.ImageNotFound:
            return None

    def get_latest_image_id_for_service(self, service_name):
        image = self.get_latest_image_for_service(service_name)
        if image is not None:
            return image.id
        return None

    def get_latest_image_for_service(self, service_name):
        try:
            image = self.client.images.get(
                '%s:latest' % self.image_name_for_service(service_name))
        except docker_errors.ImageNotFound:
            images = self.client.images.list(name=self.image_name_for_service(service_name))
            logger.debug(
                u"Could not find the latest image for service, "
                u"searching for other tags with same image name",
                image_name=self.image_name_for_service(service_name),
                service=service_name)

            if not images:
                return None

            def tag_sort(i):
                return [t for t in i.tags if t.startswith(self.image_name_for_service(service_name))][0]

            images = sorted(images, key=tag_sort)
            logger.debug('Found images for service',
                         service=service_name, images=images)
            return images[-1]
        else:
            return image

    def containers_built_for_services(self, services):
        # Verify all images are built
        for service_name in services:
            logger.info(u'Verifying service image', service=service_name)
            image_id = self.get_latest_image_id_for_service(service_name)
            if image_id is None:
                raise exceptions.AnsibleContainerMissingImage(
                    u"Missing image for service '{}'. Run 'ansible-container build' to (re)create it."
                    .format(service_name)
                )

    def get_build_stamp_for_image(self, image_id):
        build_stamp = None
        try:
            image = self.client.images.get(image_id)
        except docker_errors.ImageNotFound:
            raise exceptions.AnsibleContainerConductorException(
                "Unable to find image {}".format(image_id)
            )
        if image and image.tags:
            build_stamp = [tag for tag in image.tags if not tag.endswith(':latest')][0].split(':')[-1]
        return build_stamp

    @log_runs
    @conductor_only
    def flatten_container(self,
                          container_id,
                          service_name,
                          metadata):
        image_name = self.image_name_for_service(service_name)
        image_version = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
        image_config = utils.metadata_to_image_config(metadata)

        to_squash = self.client.containers.get(container_id)
        raw_image = to_squash.export()

        logger.debug("Exported service container as tarball", container=image_name)

        out = self.client.api.import_image_from_data(
            raw_image.read(),
            repository=image_name,
            tag=image_version
        )
        logger.debug("Committed flattened image", out=out)

        image_id = json.loads(out)['status']

        self.tag_image_as_latest(service_name, image_id.split(':')[-1])

        return image_id


    @log_runs
    @conductor_only
    def commit_role_as_layer(self,
                             container_id,
                             service_name,
                             fingerprint,
                             metadata,
                             with_name=False):
        to_commit = self.client.containers.get(container_id)
        image_name = self.image_name_for_service(service_name)
        image_version = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
        image_config = utils.metadata_to_image_config(metadata)
        image_config.setdefault('Labels', {})[self.FINGERPRINT_LABEL_KEY] = fingerprint
        commit_data = dict(
            repository=image_name if with_name else None,
            tag=image_version if with_name else None,
            message=self.LAYER_COMMENT,
            conf=image_config
        )
        logger.debug('Committing new layer', params=commit_data)
        return to_commit.commit(**commit_data).id

    def tag_image_as_latest(self, service_name, image_id):
        image_obj = self.client.images.get(image_id)
        image_obj.tag(self.image_name_for_service(service_name), 'latest')

    @conductor_only
    def generate_orchestration_playbook(self, url=None, namespace=None, local_images=True, **kwargs):
        """
        Generate an Ansible playbook to orchestrate services.
        :param url: registry URL where images will be pulled from
        :param namespace: registry namespace
        :param local_images: bypass pulling images, and use local copies
        :return: playbook dict
        """
        states = ['start', 'restart', 'stop', 'destroy']

        service_def = {}
        for service_name, service in self.services.items():
            service_definition = {}
            if service.get('roles'):
                image = self.get_latest_image_for_service(service_name)
                if image is None:
                    raise exceptions.AnsibleContainerConductorException(
                        u"No image found for service {}, make sure you've run `ansible-container "
                        u"build`".format(service_name)
                    )
                service_definition[u'image'] = image.tags[0]
            else:
                try:
                    image = self.client.images.get(service['from'])
                except docker.errors.ImageNotFound:
                    image = None
                    logger.warning(u"Image {} for service {} not found. "
                                   u"An attempt will be made to pull it.".format(service['from'], service_name))
                if image:
                    service_definition[u'image'] = image.tags[0]
                else:
                    service_definition[u'image'] = service['from']
            for extra in self.COMPOSE_WHITELIST:
                if extra in service:
                    service_definition[extra] = service[extra]
            logger.debug(u'Adding new service to definition',
                         service=service_name, definition=service_definition)
            service_def[service_name] = service_definition

        tasks = []
        for desired_state in states:
            task_params = {
                u'project_name': self.project_name,
                u'definition': {
                    u'version': u'2',
                    u'services': service_def,
                }
            }
            if self.volumes:
                task_params[u'definition'][u'volumes'] = dict(self.volumes)

            if desired_state in {'restart', 'start', 'stop'}:
                task_params[u'state'] = u'present'
                if desired_state == 'restart':
                    task_params[u'restarted'] = True
                if desired_state == 'stop':
                    task_params[u'stopped'] = True
            elif desired_state == 'destroy':
                task_params[u'state'] = u'absent'
                task_params[u'remove_volumes'] = u'yes'

            tasks.append({u'docker_service': task_params, u'tags': [desired_state]})

        playbook = [{
            u'hosts': u'localhost',
            u'gather_facts': False,
            u'tasks': tasks,
        }]

        for service in list(self.services.keys()) + ['conductor']:
            image_name = self.image_name_for_service(service)
            for image in self.client.images.list(name=image_name):
                logger.debug('Found image for service', tags=image.tags, id=image.short_id)
                for tag in image.tags:
                    logger.debug('Adding task to destroy image', tag=tag)
                    playbook[0][u'tasks'].append({
                        u'docker_image': {
                            u'name': tag,
                            u'state': u'absent',
                            u'force': u'yes'
                        },
                        u'tags': u'destroy'
                    })

        logger.debug(u'Created playbook to run project', playbook=playbook)
        return playbook

    @conductor_only
    def push(self, image_id, service_name, repository_data):
        """
        Push an image to a remote registry.
        """
        tag = repository_data.get('tag')
        namespace = repository_data.get('namespace')
        url = repository_data.get('url')
        auth_config = {
            'username': repository_data.get('username'),
            'password': repository_data.get('password')
        }

        build_stamp = self.get_build_stamp_for_image(image_id)
        tag = tag or build_stamp

        repository = "%s/%s-%s" % (namespace, self.project_name, service_name)
        if url != self.default_registry_url:
            url = REMOVE_HTTP.sub('', url)
            repository = "%s/%s" % (re.sub('/$', '', url), repository)

        logger.info('Tagging %s' % repository)
        self.client.api.tag(image_id, repository, tag=tag)

        logger.info('Pushing %s:%s...' % (repository, tag))
        stream = self.client.api.push(repository, tag=tag, stream=True, auth_config=auth_config)

        last_status = None
        for data in stream:
            data = data.splitlines()
            for line in data:
                line = json.loads(line)
                if type(line) is dict and 'error' in line:
                    plainLogger.error(line['error'])
                if type(line) is dict and 'status' in line:
                    if line['status'] != last_status:
                        plainLogger.info(line['status'])
                    last_status = line['status']
                else:
                    plainLogger.debug(line)

    @log_runs
    @host_only
    def build_conductor_image(self, base_path, base_image, cache=True):
        with utils.make_temp_dir() as temp_dir:
            logger.info('Building Docker Engine context...')
            tarball_path = os.path.join(temp_dir, 'context.tar')
            tarball_file = open(tarball_path, 'wb')
            tarball = tarfile.TarFile(fileobj=tarball_file,
                                      mode='w')
            source_dir = os.path.normpath(base_path)

            for filename in ['ansible.cfg', 'ansible-requirements.txt',
                             'requirements.yml']:
                file_path = os.path.join(source_dir, filename)
                if os.path.exists(filename):
                    tarball.add(file_path,
                                arcname=os.path.join('build-src', filename))
            # Make an empty file just to make sure the build-src dir has something
            open(os.path.join(temp_dir, '.touch'), 'w')
            tarball.add(os.path.join(temp_dir, '.touch'), arcname='build-src/.touch')

            tarball.add(os.path.join(FILES_PATH, 'get-pip.py'),
                        arcname='contrib/get-pip.py')

            container_dir = os.path.dirname(container.__file__)
            tarball.add(container_dir, arcname='container-src')
            package_dir = os.path.dirname(container_dir)

            # For an editable install, the setup.py and requirements.* will be
            # available in the package_dir. Otherwise, our custom sdist (see
            # setup.py) would have moved them to FILES_PATH
            setup_py_dir = (package_dir
                            if os.path.exists(os.path.join(package_dir, 'setup.py'))
                            else FILES_PATH)
            req_txt_dir = (package_dir
                           if os.path.exists(os.path.join(package_dir, 'conductor-requirements.txt'))
                           else FILES_PATH)
            req_yml_dir = (package_dir
                           if os.path.exists(os.path.join(package_dir, 'conductor-requirements.yml'))
                           else FILES_PATH)
            tarball.add(os.path.join(setup_py_dir, 'setup.py'),
                        arcname='container-src/conductor-build/setup.py')
            tarball.add(os.path.join(req_txt_dir, 'conductor-requirements.txt'),
                            arcname='container-src/conductor-build/conductor-requirements.txt')
            tarball.add(os.path.join(req_yml_dir, 'conductor-requirements.yml'),
                        arcname='container-src/conductor-build/conductor-requirements.yml')

            utils.jinja_render_to_temp(TEMPLATES_PATH,
                                       'conductor-dockerfile.j2', temp_dir,
                                       'Dockerfile',
                                       conductor_base=base_image,
                                       docker_version=DOCKER_VERSION)
            tarball.add(os.path.join(temp_dir, 'Dockerfile'),
                        arcname='Dockerfile')

            #for context_file in ['builder.sh', 'ansible-container-inventory.py',
            #                     'ansible.cfg', 'wait_on_host.py', 'ac_galaxy.py']:
            #    tarball.add(os.path.join(TEMPLATES_PATH, context_file),
            #                arcname=context_file)

            logger.debug('Context manifest:')
            for tarinfo_obj in tarball.getmembers():
                logger.debug('tarball item: %s (%s bytes)', tarinfo_obj.name,
                             tarinfo_obj.size, file=tarinfo_obj.name,
                             bytes=tarinfo_obj.size, terse=True)
            tarball.close()
            tarball_file.close()
            tarball_file = open(tarball_path, 'rb')
            logger.info('Starting Docker build of Ansible Container Conductor image (please be patient)...')
            # FIXME: Error out properly if build of conductor fails.
            if self.debug:
                for line_json in self.client.api.build(fileobj=tarball_file,
                                                       decode=True,
                                                       custom_context=True,
                                                       tag=self.image_name_for_service('conductor'),
                                                       rm=True,
                                                       nocache=not cache):
                    try:
                        if line_json.get('status') == 'Downloading':
                            # skip over lines that give spammy byte-by-byte
                            # progress of downloads
                            continue
                        elif 'errorDetail' in line_json:
                            raise exceptions.AnsibleContainerException(
                                "Error building conductor image: {0}".format(line_json['errorDetail']['message']))
                    except ValueError:
                        pass
                    except exceptions.AnsibleContainerException:
                        raise

                    # this bypasses the fancy colorized logger for things that
                    # are just STDOUT of a process
                    plainLogger.debug(text.to_text(line_json.get('stream', json.dumps(line_json))).rstrip())
                return self.get_latest_image_id_for_service('conductor')
            else:
                image = self.client.images.build(fileobj=tarball_file,
                                                 custom_context=True,
                                                 tag=self.image_name_for_service('conductor'),
                                                 rm=True,
                                                 nocache=not cache)
                return image.id

    def get_runtime_volume_id(self, mount_point):
        try:
            container_data = self.client.api.inspect_container(
                self.container_name_for_service('conductor')
            )
        except docker_errors.APIError:
            raise ValueError('Conductor container not found.')
        mounts = container_data['Mounts']
        try:
            usr_mount, = [mount for mount in mounts if mount['Destination'] == mount_point]
        except ValueError:
            raise ValueError('Runtime volume %s not found on Conductor' % mount_point)
        return usr_mount['Name']

    @host_only
    def import_project(self, base_path, import_from, bundle_files=False, **kwargs):
        from .importer import DockerfileImport

        dfi = DockerfileImport(base_path,
                               self.project_name,
                               import_from,
                               bundle_files)
        dfi.run()

    @conductor_only
    def login(self, username, password, email, url, config_path):
        """
        If username and password are provided, authenticate with the registry.
        Otherwise, check the config file for existing authentication data.
        """
        if username and password:
            try:
                self.client.login(username=username, password=password, email=email,
                                  registry=url, reauth=True)
            except docker_errors.APIError as exc:
                raise exceptions.AnsibleContainerConductorException(
                    u"Error logging into registry: {}".format(exc)
                )
            except Exception:
                raise

            self._update_config_file(username, password, email, url, config_path)

        username, password = self._get_registry_auth(url, config_path)
        if not username:
            raise exceptions.AnsibleContainerConductorException(
                u'Please provide login credentials for registry {}.'.format(url))
        return username, password

    @staticmethod
    @conductor_only
    def _update_config_file(username, password, email, url, config_path):
        """Update the config file with the authorization."""
        try:
            # read the existing config
            config = json.load(open(config_path, "r"))
        except ValueError:
            config = dict()

        if not config.get('auths'):
            config['auths'] = dict()

        if not config['auths'].get(url):
            config['auths'][url] = dict()
        encoded_credentials = dict(
            auth=base64.b64encode(username + b':' + password),
            email=email
        )
        config['auths'][url] = encoded_credentials
        try:
            json.dump(config, open(config_path, "w"), indent=5, sort_keys=True)
        except Exception as exc:
            raise exceptions.AnsibleContainerConductorException(
                u"Failed to write registry config to {0} - {1}".format(config_path, exc)
            )

    @staticmethod
    @conductor_only
    def _get_registry_auth(registry_url, config_path):
        """
        Retrieve from the config file the current authentication for a given URL, and
        return the username, password
        """
        username = None
        password = None
        try:
            docker_config = json.load(open(config_path))
        except ValueError:
            # The configuration file is empty
            return username, password
        if docker_config.get('auths'):
            docker_config = docker_config['auths']
        auth_key = docker_config.get(registry_url, {}).get('auth', None)
        if auth_key:
            username, password = base64.b64decode(auth_key).split(':', 1)
        return username, password
