import importlib.metadata

if __package__ is None:
    msg = '__package__ is not set'
    raise RuntimeError(msg)
__version__ = importlib.metadata.version(__package__)
