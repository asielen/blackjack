__author__ = 'andrew.sielen'

# external
import arrow

# Internal - Should have none outside system base
from system import logger
if __name__ == "__main__": logger.setup_logger()

__version__ = 200
# Basic timer system v2.0

class process_timer():
    def __init__(self, name="", total_tasks=None, verbose=True):
        logger.log_info("Timer {} Started".format(name))
        self.name = name
        self.start_time = arrow.now()
        self.tasks = 0
        self.total_tasks = total_tasks
        self.verbose = verbose

    def _get_run_time(self):
        time_diff = arrow.now() - self.start_time
        return time_diff.seconds

    def _update_tasks(self, num_of_tasks):
        self.tasks += num_of_tasks

    @property
    def tasks_completed(self):
        return self.tasks

    @property
    def tasks_remaining(self):
        if self.total_tasks is None:
            return None
        else:
            return self.total_tasks-self.tasks_completed

    def end(self):
        time_diff = self._get_run_time()
        logger.log_info("@ Run Time: {} seconds".format(time_diff))
        logger.log_info("Timer {} Ended".format(self.name))
        del self

    def log_time(self, num_of_tasks): # num_of_tasks is number of last completed tasks
        time_diff = self._get_run_time()
        self._update_tasks(num_of_tasks)
        if self.verbose is True or (self.tasks_remaining is None and self.verbose is False):
            logger.log_info("@ Process Time: {} seconds FOR {} objects processed".format(time_diff, self.tasks))
        tasks_per_second = self.tasks / max(1, time_diff)
        if self.verbose:
            logger.log_info(
                "@@ Process Time: {} per min IS {} objects per second".format(round(60 * tasks_per_second),
                                                                              round(tasks_per_second)))
        if self.tasks_remaining is not None:
            logger.log_info(
                "@@ Process Time: ETR: {} mins FOR {} objects".format(round(self.tasks_remaining / (60 * tasks_per_second)),
                                                                      self.tasks_remaining))