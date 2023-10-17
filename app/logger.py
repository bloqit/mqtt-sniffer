import logging
import sys
import os

from logging.handlers import RotatingFileHandler
import json_log_formatter
    
class Logger: 
    def __init__(self, name, log_dir, filename, logging_level=logging.DEBUG):
        
        # set log
        formatter = json_log_formatter.JSONFormatter()

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging_level)

        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(formatter)
        self.logger.addHandler(streamHandler)

        rotatingFileHandler = RotatingFileHandler(os.path.join(log_dir, filename), maxBytes=(1*1024*1024), backupCount=1)
        rotatingFileHandler.setFormatter(formatter)
        self.logger.addHandler(rotatingFileHandler)

    def debug(self, msg, extra=None):
        if extra is not None:
            self.logger.debug(msg, extra=extra)
        else:
            self.logger.debug(msg)

    def info(self, msg, extra=None):
        if extra is not None:
            self.logger.info(msg, extra=extra)
        else:
            self.logger.info(msg)

    def warning(self, msg, extra=None):
        if extra is not None:
            self.logger.warning(msg, extra=extra)
        else:
            self.logger.warning(msg)

    def error(self, msg, extra=None):
        if extra is not None:
            self.logger.error(msg, extra=extra)
        else:
            self.logger.error(msg)
    
    def critical(self, msg, extra=None):
        if extra is not None:
            self.logger.critical(msg, extra=extra)
        else:
            self.logger.critical(msg)
    
    def exception(self, msg, extra=None):
        if extra is not None:
            self.logger.exception(msg, extra=extra)
        else:
            self.logger.exception(msg)
