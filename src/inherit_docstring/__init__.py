from .decorator import inherit_docstring

__all__ = ['__version__', 'inherit_docstring']


def __getattr__(name: str) -> str:
    if name == '__version__':
        from .version import __version__

        return __version__
    msg = f'module {__name__} has no attribute {name}'
    raise AttributeError(msg)
