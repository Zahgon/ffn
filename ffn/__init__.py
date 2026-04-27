from . import core, data
from .core import *
from .data import get

try:
    core.extend_pandas()
except Exception:
    pass

__version__ = "1.1.5"
