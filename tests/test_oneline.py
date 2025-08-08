from __future__ import annotations

from inherit_docstring import inherit_docstring

from .utils import add_indent


class ParentOneline:
    """Parent class with oneline docstring."""

    def func() -> None:
        """Function with oneline docstring."""


def test_parent_oneline_class() -> None:
    assert ParentOneline.__doc__ == 'Parent class with oneline docstring.'


def test_parent_oneline_func() -> None:
    assert ParentOneline.func.__doc__ == 'Function with oneline docstring.'


@inherit_docstring
class ChildOneline(ParentOneline):
    """Child class with oneline docstring."""

    def func() -> None:
        """Function with oneline docstring."""


def test_child_oneline_class() -> None:
    assert ChildOneline.__doc__ == 'Child class with oneline docstring.'


def test_child_oneline_func() -> None:
    assert ChildOneline.func.__doc__ == 'Function with oneline docstring.'


@inherit_docstring
class ChildMultiline(ParentOneline):
    """Child class with multiline docstring.

    This is child.

    Attributes
    ----------
    name : str
        The name of
        the child.
    child_attr : int
        The child attribute.

    Notes
    -----
    This is child note.

    Examples
    --------
    This is example.

    """

    def func1(self, a: str, b: int, c: float) -> int:
        """Function 1.

        Parameters
        ----------
        a : str
            The first parameter in child.
            Yes, it is.

        """
        return 1.1


def test_child_multiline_class() -> None:
    assert ChildMultiline.__doc__ == add_indent(
        """Child class with multiline docstring.

This is child.

Attributes
----------
name : str
    The name of
    the child.
child_attr : int
    The child attribute.

Notes
-----
This is child note.

Examples
--------
This is example.

""",
        'class',
    )


def test_child_multiline_func() -> None:
    assert ChildMultiline.func1.__doc__ == add_indent(
        """Function 1.

Parameters
----------
a : str
    The first parameter in child.
    Yes, it is.

""",
        'func',
    )


@inherit_docstring
class ChildMultiHeader(ParentOneline):
    """Child class with multiline header.

    This is child.

    """


def test_child_multiheader_class() -> None:
    assert ChildMultiHeader.__doc__ == add_indent(
        """Child class with multiline header.

This is child.

""",
        'class',
    )


@inherit_docstring
class ChildMultiHeaderNoBlankLine(ParentOneline):
    """Child class with multiline header without last blank line.

    This is child.
    """


def test_child_multiheader_no_blank_line_class() -> None:
    assert ChildMultiHeaderNoBlankLine.__doc__ == add_indent(
        """Child class with multiline header without last blank line.

This is child.
""",
        'class',
    )
