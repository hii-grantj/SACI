__version__ = "0.0.0"

import logging
logging.getLogger("saci").addHandler(logging.NullHandler())
from .loggingconf import Loggers
loggers = Loggers()
del Loggers
del logging
