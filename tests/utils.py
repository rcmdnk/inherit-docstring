import sys


def add_indent(docstring: str, docstring_type: str = 'class') -> str:
    if sys.version_info < (3, 13):
        indent = 4 if docstring_type == 'class' else 8
        docstring = '\n'.join(
            [' ' * indent + x if x else '' for x in docstring.split('\n')]
        )
        if docstring.endswith('\n'):
            docstring += ' ' * indent

    return docstring.lstrip()
