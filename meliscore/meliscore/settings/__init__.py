from dev import *

try:
    from .local import *
except ImportError, e:
    # 'Unable to load local.py:', e
    pass
