import sys

from .utils import merge_docstring

CLASS_INDENT = 4 if sys.version_info < (3, 13) else 0
FUNC_INDENT = 8 if sys.version_info < (3, 13) else 0


def inherit_docstring(cls: type) -> type:
    doc = cls.__doc__ if cls.__doc__ is not None else ''
    base_doc = ''
    for base in cls.__bases__:
        if base.__doc__ is not None:
            base_doc = base.__doc__
            break
    cls.__doc__ = merge_docstring(base_doc, doc, indent=CLASS_INDENT)

    for name, method in cls.__dict__.items():
        if callable(method):
            doc = method.__doc__ if method.__doc__ is not None else ''
            base_doc = ''
            for base in cls.__bases__:
                if (
                    hasattr(base, name)
                    and getattr(base, name).__doc__ is not None
                ):
                    base_doc = getattr(base, name).__doc__
                    break
            method.__doc__ = merge_docstring(base_doc, doc, indent=FUNC_INDENT)

    return cls
