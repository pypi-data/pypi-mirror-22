import syslog
from abc import ABCMeta, abstractmethod
from easy_alert.util.case_class import CaseClass


class Logger(CaseClass):
    """abstract logger class"""

    __metaclass__ = ABCMeta

    def __init__(self, ident):
        """
        :param ident: identity for logger
        """
        super(Logger, self).__init__(['ident'])
        self.ident = ident

    def info(self, message):
        self._log_message(syslog.LOG_INFO, message)

    def warn(self, message):
        self._log_message(syslog.LOG_WARNING, message)

    def error(self, message):
        self._log_message(syslog.LOG_ERR, message)

    def traceback(self):
        """do nothing by default"""

    def _log_message(self, priority, message):
        prefix = {
            syslog.LOG_INFO: '[INFO] ',
            syslog.LOG_WARNING: '[WARN] ',
            syslog.LOG_ERR: '[ERROR]'
        }[priority]
        msg = '%s%s' % (prefix, message)
        self._log(priority, msg)

    @abstractmethod
    def _log(self, priority, message):
        """log raw message"""
