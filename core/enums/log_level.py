from enum import Enum

class LogLevel(Enum):
    '''Enum for log levels, used by the LogService.'''
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5