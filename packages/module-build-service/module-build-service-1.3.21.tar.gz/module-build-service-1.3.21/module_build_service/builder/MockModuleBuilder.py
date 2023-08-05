# -*- coding: utf-8 -*-
# Copyright (c) 2016  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Jan Kaluža <jkaluza@redhat.com>


import logging
import os
import koji
import kobo.rpmlib
import shutil
import yaml
import threading

from module_build_service import conf, log, db
import module_build_service.scm
import module_build_service.utils
import module_build_service.scheduler
import module_build_service.scheduler.consumer

from base import GenericBuilder
from utils import (build_from_scm, fake_repo_done_message,
                   create_local_repo_from_koji_tag, execute_cmd)
from KojiModuleBuilder import KojiModuleBuilder
from module_build_service.models import ModuleBuild

logging.basicConfig(level=logging.DEBUG)


class MockModuleBuilder(GenericBuilder):
    """
    See http://blog.samalik.com/copr-in-the-modularity-world/
    especially section "Building a stack"
    """

    backend = "mock"
    # Global build_id/task_id we increment when new build is executed.
    _build_id_lock = threading.Lock()
    _build_id = 1
    _config_lock = threading.Lock()

    MOCK_CONFIG_TEMPLATE = """
config_opts['root'] = '$root'
config_opts['target_arch'] = '$arch'
config_opts['legal_host_arches'] = ('$arch',)
config_opts['chroot_setup_cmd'] = 'install $group'
config_opts['dist'] = ''
config_opts['extra_chroot_dirs'] = [ '/run/lock', ]
config_opts['releasever'] = ''
config_opts['package_manager'] = 'dnf'
config_opts['nosync'] = True

config_opts['yum.conf'] = \"\"\"
$yum_conf
\"\"\"
"""

    MOCK_YUM_CONF_TEMPLATE = """
[main]
keepcache=1
debuglevel=2
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=
install_weak_deps=0
metadata_expire=3600
mdpolicy=group:primary

# repos

"""

    @module_build_service.utils.validate_koji_tag('tag_name')
    def __init__(self, owner, module, config, tag_name, components):
        self.module_str = module.name
        self.tag_name = tag_name
        self.config = config
        self.groups = []
        self.arch = "x86_64" # TODO: We may need to change that in the future
        self.yum_conf = MockModuleBuilder.MOCK_YUM_CONF_TEMPLATE

        # Create main directory for this tag
        self.tag_dir = os.path.join(self.config.mock_resultsdir, tag_name)
        if not os.path.exists(self.tag_dir):
            os.makedirs(self.tag_dir)

        # Create "results" sub-directory for this tag to store build results
        # and local repository.
        self.resultsdir = os.path.join(self.tag_dir, "results")
        if not os.path.exists(self.resultsdir):
            os.makedirs(self.resultsdir)

        # Create "config" sub-directory.
        self.configdir = os.path.join(self.tag_dir, "config")
        if not os.path.exists(self.configdir):
            os.makedirs(self.configdir)

        # Generate path to mock config and add local repository there.
        self._add_repo("localrepo", "file://" + self.resultsdir, "metadata_expire=1\n")

        # Remove old files from the previous build of this tag but only
        # before the first build is done, otherwise we would remove files
        # which we already build in this module build.
        if MockModuleBuilder._build_id == 1:
            # Remove all RPMs from the results directory, but keep old logs.
            for name in os.listdir(self.resultsdir):
                if name.endswith(".rpm"):
                    os.remove(os.path.join(self.resultsdir, name))

            # Remove the old RPM repository from the results directory.
            if os.path.exists(os.path.join(self.resultsdir, "repodata/repomd.xml")):
                os.remove(os.path.join(self.resultsdir, "repodata/repomd.xml"))

            # Remove old config files from config directory.
            for name in os.listdir(self.configdir):
                os.remove(os.path.join(self.configdir, name))

        log.info("MockModuleBuilder initialized, tag_name=%s, tag_dir=%s" %
                 (tag_name, self.tag_dir))

    @property
    def module_build_tag(self):
        # Workaround koji specific code in modules.py
        return {"name": self.tag_name}

    def _createrepo(self):
        """
        Creates the repository using "createrepo_c" command in the resultsdir.
        """
        log.debug("Creating repository in %s" % self.resultsdir)
        path = self.resultsdir
        repodata_path = os.path.join(path, "repodata")

        # Remove old repodata files
        if os.path.exists(repodata_path):
            for name in os.listdir(repodata_path):
                os.remove(os.path.join(repodata_path, name))

        # Generate the mmd the same way as pungi does.
        m1 = ModuleBuild.query.filter(ModuleBuild.name == self.module_str).one()
        modules = {"modules": []}
        modules["modules"].append(yaml.safe_load(m1.mmd().dumps()))
        mmd_path = os.path.join(path, "modules.yaml")

        with open(mmd_path, "w") as outfile:
            outfile.write(yaml.safe_dump(modules))

        # Generate repo and inject modules.yaml there.
        execute_cmd(['/usr/bin/createrepo_c', path])
        execute_cmd(['/usr/bin/modifyrepo_c', '--mdtype=modules', mmd_path, repodata_path])

    def _add_repo(self, name, baseurl, extra=""):
        """
        Adds repository to Mock config file. Call _write_mock_config() to
        actually write the config file to filesystem.
        """
        self.yum_conf += "[%s]\n" % name
        self.yum_conf += "name=%s\n" % name
        self.yum_conf += "baseurl=%s\n" % baseurl
        self.yum_conf += extra
        self.yum_conf += "enabled=1\n"

    def _load_mock_config(self):
        """
        Loads the variables which are generated only during the first
        initialization of mock config. This should be called before
        every _write_mock_config otherwise we overwrite Mock
        repositories or groups ...
        """

        # We do not want to load old file from previous builds here, so if
        # this is the first build in this module, skip the load completely.
        if MockModuleBuilder._build_id == 1:
            return

        with MockModuleBuilder._config_lock:
            infile = os.path.join(self.configdir, "mock.cfg")
            with open(infile, 'r') as f:
                # This looks scary, but it is the way how mock itself loads the
                # config file ...
                config_opts = {}
                code = compile(f.read(), infile, 'exec')
                # pylint: disable=exec-used
                exec(code)

                self.groups = config_opts["chroot_setup_cmd"].split(" ")[1:]
                self.yum_conf = config_opts['yum.conf']

    def _write_mock_config(self):
        """
        Writes Mock config file to local file.
        """

        with MockModuleBuilder._config_lock:
            config = str(MockModuleBuilder.MOCK_CONFIG_TEMPLATE)
            config = config.replace("$root", "%s-%s" % (self.tag_name,
                                                        str(threading.current_thread().name)))
            config = config.replace("$arch", self.arch)
            config = config.replace("$group", " ".join(self.groups))
            config = config.replace("$yum_conf", self.yum_conf)

            # We write the most recent config to "mock.cfg", so thread-related
            # configs can be later (re-)generated from it using _load_mock_config.
            outfile = os.path.join(self.configdir, "mock.cfg")
            with open(outfile, 'w') as f:
                f.write(config)

            # Write the config to thread-related configuration file.
            outfile = os.path.join(self.configdir, "mock-%s.cfg" %
                                   str(threading.current_thread().name))
            with open(outfile, 'w') as f:
                f.write(config)

    def buildroot_connect(self, groups):
        self._load_mock_config()
        self.groups = list(set().union(groups["build"], self.groups))
        log.debug("Mock builder groups: %s" % self.groups)
        self._write_mock_config()

    def buildroot_prep(self):
        pass

    def buildroot_resume(self):
        pass

    def buildroot_ready(self, artifacts=None):
        return True

    def buildroot_add_dependency(self, dependencies):
        pass

    def buildroot_add_artifacts(self, artifacts, install=False):
        self._createrepo()

        # TODO: This is just hack to install module-build-macros into the
        # buildroot. We should really install the RPMs belonging to the
        # right source RPM into the buildroot here, but we do not track
        # what RPMs are output of particular SRPM build yet.
        for artifact in artifacts:
            if artifact and artifact.startswith("module-build-macros"):
                self._load_mock_config()
                self.groups.append("module-build-macros")
                self._write_mock_config()

        fake_repo_done_message(self.tag_name)

    def tag_artifacts(self, artifacts):
        pass

    def buildroot_add_repos(self, dependencies):
        # TODO: We support only dependencies from Koji here. This should be
        # extended to Copr in the future.
        self._load_mock_config()
        for tag in dependencies:
            repo_dir = os.path.join(self.config.cache_dir, "koji_tags", tag)
            create_local_repo_from_koji_tag(self.config, tag, repo_dir,
                                            [self.arch, "noarch"])
            baseurl = "file://" + repo_dir
            self._add_repo(tag, baseurl)
        self._write_mock_config()

    def _send_build_change(self, state, source, build_id):
        nvr = kobo.rpmlib.parse_nvr(source)

        # build_id=1 and task_id=1 are OK here, because we are building just
        # one RPM at the time.
        msg = module_build_service.messaging.KojiBuildChange(
            msg_id='a faked internal message',
            build_id=build_id,
            task_id=build_id,
            build_name=nvr["name"],
            build_new_state=state,
            build_release=nvr["release"],
            build_version=nvr["version"]
        )
        module_build_service.scheduler.consumer.work_queue_put(msg)

    def _save_log(self, resultsdir, log_name, artifact_name):
        old_log = os.path.join(resultsdir, log_name)
        new_log = os.path.join(resultsdir, artifact_name + "-" + log_name)
        if os.path.exists(old_log):
            os.rename(old_log, new_log)

    def build_srpm(self, artifact_name, source, build_id):
        """
        Builds the artifact from the SRPM.
        """
        state = koji.BUILD_STATES['BUILDING']

        # Use the mock config associated with this thread.
        mock_config = os.path.join(self.configdir,
                                   "mock-%s.cfg" % str(threading.current_thread().name))

        # Clear resultsdir associated with this thread or in case it does not
        # exist, create it.
        resultsdir = os.path.join(self.resultsdir,
                                  str(threading.current_thread().name))
        if os.path.exists(resultsdir):
            for name in os.listdir(resultsdir):
                os.remove(os.path.join(resultsdir, name))
        else:
            os.makedirs(resultsdir)

        # Open the logs to which we will forward mock stdout/stderr.
        mock_stdout_log = open(os.path.join(self.resultsdir,
                                            artifact_name + "-mock-stdout.log"), "w")
        mock_stderr_log = open(os.path.join(self.resultsdir,
                                            artifact_name + "-mock-stderr.log"), "w")

        try:
            # Initialize mock.
            execute_cmd(["mock", "-v", "-r", mock_config, "--init"],
                        stdout=mock_stdout_log, stderr=mock_stderr_log)

            # Start the build and store results to resultsdir
            execute_cmd(["mock", "-v", "-r", mock_config,
                          "--no-clean", "--rebuild", source,
                          "--resultdir=%s" % resultsdir],
                        stdout=mock_stdout_log, stderr=mock_stderr_log)

            # Emit messages simulating complete build. These messages
            # are put in the scheduler's work queue and are handled
            # by MBS after the build_srpm() method returns and scope gets
            # back to scheduler.main.main() method.
            state = koji.BUILD_STATES['COMPLETE']
            self._send_build_change(state, source, build_id)

            with open(os.path.join(resultsdir, "status.log"), 'w') as f:
                f.write("complete\n")
        except Exception as e:
            log.error("Error while building artifact %s: %s" % (artifact_name,
                                                                str(e)))

            # Emit messages simulating complete build. These messages
            # are put in the scheduler's work queue and are handled
            # by MBS after the build_srpm() method returns and scope gets
            # back to scheduler.main.main() method.
            state = koji.BUILD_STATES['FAILED']
            self._send_build_change(state, source,
                                    build_id)
            with open(os.path.join(resultsdir, "status.log"), 'w') as f:
                f.write("failed\n")

        mock_stdout_log.close()
        mock_stderr_log.close()

        self._save_log(resultsdir, "state.log", artifact_name)
        self._save_log(resultsdir, "root.log", artifact_name)
        self._save_log(resultsdir, "build.log", artifact_name)
        self._save_log(resultsdir, "status.log", artifact_name)

        # Copy files from thread-related resultsdire to the main resultsdir.
        for name in os.listdir(resultsdir):
            shutil.copyfile(os.path.join(resultsdir, name), os.path.join(self.resultsdir, name))

        # We return BUILDING state here even when we know it is already
        # completed or failed, because otherwise utils.start_build_batch
        # would think this component is already built and also tagged, but
        # we have just built it - tagging will happen as result of build
        # change message we are sending above using _send_build_change.
        # It is just to make this backend compatible with other backends,
        # which return COMPLETE here only in case the resulting build is
        # already in repository ready to be used. This is not a case for Mock
        # backend in the time we return here.
        reason = "Building %s in Mock" % (artifact_name)
        return build_id, koji.BUILD_STATES['BUILDING'], reason, None

    def build(self, artifact_name, source):
        log.info("Starting building artifact %s: %s" % (artifact_name, source))

        # Load global mock config for this module build from mock.cfg and
        # generate the thread-specific mock config by writing it to fs again.
        self._load_mock_config()
        self._write_mock_config()

        # Get the build-id in thread-safe manner.
        build_id = None
        with MockModuleBuilder._build_id_lock:
            MockModuleBuilder._build_id += 1
            build_id = int(MockModuleBuilder._build_id)

        # Git sources are treated specially.
        if source.startswith("git://"):
            # Open the srpm-stdout and srpm-stderr logs and build from SCM.
            srpm_stdout_fn = os.path.join(self.resultsdir,
                                          artifact_name + "-srpm-stdout.log")
            srpm_stderr_fn = os.path.join(self.resultsdir,
                                          artifact_name + "-srpm-stderr.log")
            with open(srpm_stdout_fn, "w") as srpm_stdout_log, open(srpm_stderr_fn, "w") as srpm_stderr_log:
                return build_from_scm(artifact_name, source,
                                      self.config, self.build_srpm, data=build_id,
                                      stdout=srpm_stdout_log, stderr=srpm_stderr_log)
        else:
            return self.build_srpm(artifact_name, source, build_id)

    @staticmethod
    def get_disttag_srpm(disttag, module_build):
        # @FIXME
        return KojiModuleBuilder.get_disttag_srpm(disttag, module_build)

    def cancel_build(self, task_id):
        pass

    def list_tasks_for_components(self, component_builds=None, state='active'):
        pass



