import socket
from time import sleep
import threading
import traceback
import os
from subprocess import Popen
import math

from brome.core.utils import (
    DbSessionContext,
    utcnow
)
from brome.core.settings import BROME_CONFIG
from brome.runner.base_runner import BaseRunner
from brome.model.testbatch import Testbatch
from brome.runner import ec2_instance
from brome.runner import virtualbox_instance
from brome.runner import browserstack_instance
from brome.runner import localhost_instance
from brome.runner import saucelabs_instance
from brome.runner.browser_config import BrowserConfig


class GridRunner(BaseRunner):
    """ GridRunner run on Ec2, Virtualbox,
        Browserstack, saucelabs and also localhost
    """
    def __init__(self, *args):
        super(GridRunner, self).__init__(*args)

        self.selenium_pid = None
        self.instances_ip = {}
        self.instances = {}
        self.alive_instances = []
        self.xvfb_pids = []
        self.browser_configs = {}

    def execute(self):
        """Execute the test batch
        """

        try:
            # START SELENIUM GRID
            if BROME_CONFIG['grid_runner']['start_selenium_server']:
                self.start_selenium_server()

            # Get all the browsers id
            self.browsers_id = BROME_CONFIG['runner_args']['remote_runner'].split(',')  # noqa

            # Start all the instances
            instance_threads = []
            for i, browser_id in enumerate(self.browsers_id):
                browser_config = BrowserConfig(
                    runner=self,
                    browser_id=browser_id,
                    browsers_config=BROME_CONFIG['browsers_config']
                )

                self.browser_configs[browser_id] = browser_config

                # EC2
                if browser_config.location == 'ec2':

                    max_number_of_instance = browser_config.get(
                        'max_number_of_instance'
                    )
                    nb_browser_by_instance = browser_config.get(
                        'nb_browser_by_instance'
                    )

                    if len(self.tests) < \
                            max_number_of_instance * \
                            nb_browser_by_instance:

                        nb_instance_to_launch = int(
                            math.ceil(
                                float(len(self.tests))/nb_browser_by_instance
                            )
                        )

                    else:
                        nb_instance_to_launch = max_number_of_instance

                    for j in range(nb_instance_to_launch):
                        _ec2_instance = ec2_instance.EC2Instance(
                            runner=self,
                            browser_config=browser_config,
                            index=j
                        )

                        ec2_instance_thread = InstanceThread(_ec2_instance)
                        ec2_instance_thread.start()

                        instance_threads.append(ec2_instance_thread)

                # VIRTUALBOX
                elif browser_config.location == 'virtualbox':
                    vbox_instance = virtualbox_instance.VirtualboxInstance(
                        runner=self,
                        browser_config=browser_config,
                        index=i,
                    )

                    vbox_instance_thread = InstanceThread(vbox_instance)
                    vbox_instance_thread.start()

                    instance_threads.append(vbox_instance_thread)

                # SAUCELABS
                elif browser_config.location == 'saucelabs':

                    if not self.instances.get(browser_id):
                        self.instances[browser_id] = []

                    self.instances[browser_id].append(
                        saucelabs_instance.SauceLabsInstance()
                    )

                # BROWSERSTACK
                elif browser_config.location == 'browserstack':

                    if not self.instances.get(browser_id):
                        self.instances[browser_id] = []

                    self.instances[browser_id].append(
                        browserstack_instance.BrowserstackInstance()
                    )

                # LOCALHOST
                elif browser_config.location == 'localhost':

                    max_number_of_instance = browser_config.get(
                        'max_number_of_instance', 1
                    )

                    if len(self.tests) < max_number_of_instance:
                        nb_instance_to_launch = len(self.tests)
                    else:
                        nb_instance_to_launch = max_number_of_instance

                    for i in range(0, nb_instance_to_launch):
                        if not self.instances.get(browser_id):
                            self.instances[browser_id] = []

                        self.instances[browser_id].append(
                            localhost_instance.LocalhostInstance(
                                self,
                                browser_config,
                                test_name=i
                            )
                        )

            # MILESTONE
            if len(instance_threads):
                with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                    test_batch = session.query(Testbatch)\
                        .filter(Testbatch.mongo_id == self.test_batch_id).one()
                    test_batch.add_milestone(
                        'NbInstanceToSetup',
                        {'nb': len(instance_threads)}
                    )
                    session.save(test_batch, safe=True)

            for t in instance_threads:
                t.join()

            self.info_log("The test batch is now ready!")

            # MILESTONE
            if len(instance_threads):
                with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                    test_batch = session.query(Testbatch)\
                        .filter(Testbatch.mongo_id == self.test_batch_id).one()
                    test_batch.add_milestone('InstanceSetupCompleted')
                    session.save(test_batch, safe=True)

            try:
                self.run()
            except:
                tb = traceback.format_exc()
                self.error_log(
                    "Exception in run of the grid runner: %s"
                    % str(tb)
                )
                raise

            finally:
                try:
                    self.tear_down_instances()

                    # MILESTONE
                    with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                        test_batch = session.query(Testbatch)\
                            .filter(Testbatch.mongo_id == self.test_batch_id)\
                            .one()
                        test_batch.add_milestone('InstanceTearDownCompleted')
                        session.save(test_batch, safe=True)

                    # Kill selenium server
                    if BROME_CONFIG['grid_runner']['kill_selenium_server']:  # noqa
                        if self.selenium_pid:
                            self.kill_pid(self.selenium_pid)

                            # MILESTONE
                            with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                                test_batch = session.query(Testbatch)\
                                    .filter(Testbatch.mongo_id == self.test_batch_id).one()  # noqa
                                test_batch.add_milestone(
                                    'SeleniumServerKilled'
                                )
                                session.save(test_batch, safe=True)

                    # Kill xvfb process
                    for xvfb_pid in self.xvfb_pids:
                        self.kill_pid(xvfb_pid)

                except:
                    tb = traceback.format_exc()
                    self.error_log("Exception in finally block of the grid runner: %s" % str(tb))  # noqa
        except:
            self.set_ending_timestamp()
            tb = traceback.format_exc()
            self.error_log("Exception in finally block of the grid runner: %s" % str(tb))  # noqa
            raise

        self.info_log("The test batch is finished.")

    def resolve_instance_by_ip(self, ip):
        """Resolve an instance by his ip
        """
        return self.instances_ip[ip]

    def run(self):
        """Run all the test in the test batch
        """

        executed_tests = []
        try:

            active_thread = 0
            start_thread = True
            current_index = 0
            active_thread_by_browser_id = {}

            test_index_by_browser_id = {}
            for browser_id in self.browsers_id:
                test_index_by_browser_id[browser_id] = 0

            self.kill_test_batch_if_necessary()

            while active_thread or start_thread:
                start_thread = False

                self.kill_test_batch_if_necessary()

                for browser_id in self.browsers_id:

                    if active_thread_by_browser_id.get(browser_id) is None:
                        active_thread_by_browser_id[browser_id] = 0
                    else:
                        current_active_thread = 0
                        for thread in threading.enumerate():

                            # Make sure that the thread is TestThread
                            if hasattr(thread, 'test'):
                                if thread.test._browser_config.browser_id == browser_id:  # noqa
                                    current_active_thread += 1

                        active_thread_by_browser_id[browser_id] = current_active_thread  # noqa

                    for j in range(0, len(self.instances[browser_id]) - active_thread_by_browser_id[browser_id]):  # noqa

                        self.kill_test_batch_if_necessary()

                        if test_index_by_browser_id[browser_id] < len(self.tests):  # noqa
                            current_index += 1

                            test = self.tests[test_index_by_browser_id[browser_id]]  # noqa

                            test_index_by_browser_id[browser_id] += 1

                            test_ = test.Test(
                                runner=self,
                                test_batch_id=self.test_batch_id,
                                browser_config=self.browser_configs[browser_id],  # noqa
                                name=test.Test.name,
                                index=test_index_by_browser_id[browser_id]
                            )
                            test_.pdriver.embed_disabled = True

                            thread = TestThread(test_)
                            thread.start()

                            executed_tests.append(test_)

                active_thread = len([tn for tn in threading.enumerate() if type(tn) != threading._MainThread and hasattr(tn, 'test')])  # noqa
                # self.info_log("active_thread=%s" % active_thread)
                if active_thread:
                    try:
                        active_thread_test_number = len([tn for tn in threading.enumerate() if type(tn) != threading._MainThread and hasattr(tn, 'test')])  # noqa
                        self.info_log("Active thread number: %s" % active_thread_test_number)  # noqa
                        self.info_log("Active thread name: %s" % (', '.join([  # noqa
                                "%s-%s" % (
                                    th.test._browser_config.browser_id,
                                    th.test._name
                                ) for th in threading.enumerate() if type(th) != threading._MainThread and hasattr(th, 'test')  # noqa
                            ])
                        ))
                    except Exception as e:
                        self.error_log("print active exception: %s" % str(e))

                # TIMEOUT
                now = utcnow()
                if (self.starting_timestamp - now).total_seconds() >\
                        BROME_CONFIG['grid_runner']['max_running_time']:

                    self.error_log("max_running_time reached... terminating!")
                    raise TestRunnerKilledException()

                self.kill_test_batch_if_necessary()

                sleep(10)

        except TestRunnerKilledException:
            pass

        except Exception:
            tb = traceback.format_exc()
            self.error_log("Run exception: %s" % str(tb))

        self.set_ending_timestamp()

        self.print_test_summary(executed_tests)

    def set_ending_timestamp(self):
        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_batch = session.query(Testbatch)\
                .filter(Testbatch.mongo_id == self.test_batch_id).one()
            test_batch.ending_timestamp = utcnow()
            test_batch.terminated = True
            session.save(test_batch, safe=True)

    def kill_test_batch_if_necessary(self):
        """Kill the test batch

            If the test_batch.killed is set to true
            then the test batch will be kill
        """
        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_batch = session.query(Testbatch)\
                .filter(Testbatch.mongo_id == self.test_batch_id).one()
            if test_batch.killed:
                test_batch.add_milestone('TerminatingTestBatch')
                session.save(test_batch, safe=True)

                self.info_log("Killing itself")
                for t in [t for t in threading.enumerate() if type(t) != threading._MainThread]:  # noqa
                    if not t.test.ending_timestamp:
                        self.info_log("Killing: %s" % t.test._name)
                        t.test.end()

                raise TestRunnerKilledException("Killed")

    def tear_down_instances(self):
        """Tear down all instances
        """

        self.info_log('Tearing down all instances...')

        for instance in self.alive_instances:
            instance.tear_down()

        self.info_log('[Done]Tearing down all instances')

    def start_selenium_server(self):
        """Start the selenium server
        """

        ip = BROME_CONFIG['grid_runner']['selenium_server_ip']
        port = BROME_CONFIG['grid_runner']['selenium_server_port']

        def is_selenium_server_is_running():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((ip, port))
            s.close()
            return not result

        if not is_selenium_server_is_running():
            self.info_log('Starting selenium server...')

            command = BROME_CONFIG['grid_runner']['selenium_server_command']\
                .format(
                    **BROME_CONFIG['grid_runner']
                )

            self.info_log('Selenium hub command: %s' % command)

            process = Popen(
                command.split(' '),
                stdout=open(os.path.join(self.runner_dir, "hub.log"), 'a'),
                stderr=open(os.path.join(self.runner_dir, "hub.log"), 'a'),
            )

            self.selenium_pid = process.pid

            self.info_log('Selenium server pid: %s' % self.selenium_pid)
        else:
            self.info_log('Selenium is already running.')

            # Milestone
            with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                test_batch = session.query(Testbatch)\
                    .filter(Testbatch.mongo_id == self.test_batch_id).one()  # noqa
                test_batch.add_milestone(
                    'SeleniumServerAlreadyRunning'
                )
                session.save(test_batch, safe=True)

            return True

        for i in range(30):
            self.info_log('Waiting for the selenium server to start...')
            result = is_selenium_server_is_running()

            if result:
                self.info_log('[Done]Selenium server is running.')

                # Milestone
                with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                    test_batch = session.query(Testbatch)\
                        .filter(Testbatch.mongo_id == self.test_batch_id).one()  # noqa
                    test_batch.add_milestone(
                        'SeleniumServerStarted'
                    )
                    session.save(test_batch, safe=True)

                return True
            sleep(2)

        raise Exception("Selenium server did not start!")


class InstanceThread(threading.Thread):
    """Theard that start the instance
    """

    def __init__(self, instance):
        threading.Thread.__init__(self)
        self.instance = instance
        self.runner = self.instance.runner

    def run(self):
        success = False
        try:
            success = self.instance.startup()
        except Exception as e:
            self.runner.critical_log(
                "Exception in InstanceThread instance startup: %s" % e
            )

        if not self.runner.instances.get(self.instance.browser_config.browser_id):  # noqa
            self.runner.instances[self.instance.browser_config.browser_id] = []

        if success:
            self.runner.instances[self.instance.browser_config.browser_id].append(self.instance)  # noqa
            self.runner.instances_ip[self.instance.get_ip()] = self.instance

        self.runner.alive_instances.append(self.instance)


class TestThread(threading.Thread):
    """Thread that run the test
    """

    def __init__(self, test):
        threading.Thread.__init__(self)
        self.test = test

    def run(self):
        self.test.execute()


class TestRunnerKilledException(Exception):
    """Exception that is raised when the test batch is killed
    """
    pass
