import traceback

from brome.runner.localhost_instance import LocalhostInstance
from brome.core.settings import BROME_CONFIG
from brome.runner.base_runner import BaseRunner
from brome.runner.browser_config import BrowserConfig
from brome.model.testbatch import Testbatch
from brome.core.utils import (
    utcnow,
    DbSessionContext
)


class LocalRunner(BaseRunner):
    """The local runner only run browser on localhost
    """

    def __init__(self, *args):
        super(LocalRunner, self).__init__(*args)

    def execute(self):
        """Execute the test batch
        """

        self.browser_config = BrowserConfig(
            runner=self,
            browser_id=BROME_CONFIG['runner_args']['localhost_runner'],
            browsers_config=BROME_CONFIG['browsers_config']
        )

        try:
            self.run()
        except KeyboardInterrupt:
            self.info_log("Test batch interrupted")

        except:
            tb = traceback.format_exc()
            self.error_log("Exception in run of the grid runner: %s" % str(tb))
            raise
        finally:
            self.terminate()

    def run(self):
        """Run the test batch
        """

        self.info_log("The test batch is ready.")

        self.executed_tests = []

        for test in self.tests:
            localhost_instance = LocalhostInstance(
                runner=self,
                browser_config=self.browser_config,
                test_name=test.Test.name
            )

            localhost_instance.startup()

            with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
                test_batch = session.query(Testbatch)\
                    .filter(Testbatch.mongo_id == self.test_batch_id).one()
                test_batch.total_executing_tests = 1
                session.save(test_batch, safe=True)

            test_ = test.Test(
                runner=self,
                browser_config=self.browser_config,
                name=test.Test.name,
                test_batch_id=self.test_batch_id,
                localhost_instance=localhost_instance,
                index=1
            )

            test_.execute()
            self.executed_tests.append(test_)

            localhost_instance.tear_down()

    def terminate(self):
        """Terminate the test batch
        """

        self.info_log('The test batch is finished.')

        with DbSessionContext(BROME_CONFIG['database']['mongo_database_name']) as session:  # noqa
            test_batch = session.query(Testbatch)\
                .filter(Testbatch.mongo_id == self.test_batch_id).one()
            test_batch.ending_timestamp = utcnow()
            test_batch.terminated = True
            session.save(test_batch, safe=True)

        self.print_test_summary(self.executed_tests)
