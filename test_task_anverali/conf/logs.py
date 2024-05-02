import logging
import re


class ExcludeBulkLogsFilter(logging.Filter):
    def filter(self, record):
        log_message = record.getMessage()
        if re.match(r'.*_bulk.*', log_message):
            return False
        return True
