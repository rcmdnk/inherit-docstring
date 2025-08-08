from __future__ import annotations

from inherit_docstring import inherit_docstring

from .utils import add_indent


class ParentNoBlankLine:
    """Parent class without last blank line.

    This is parent.

    Attributes
    ----------
    name : str
        The name of
        the parent.
    age
        age

    Notes
    -----
    This is note.
    """

    def func1(self, a: str, b: int, c: float) -> int:
        """Function 1.

        Parameters
        ----------
        a : str
            The first parameter.
            Yes, it is.
        b : int
            The second parameter.
            No, it is not.
        c : dict[str, int | float]
            The third parameter.
            humm...

        Returns
        -------
        ret : tuple[str, ...]
            The return value.
        """
        return 1.1


def test_parent_no_blank_line_class() -> None:
    assert ParentNoBlankLine.__doc__ == add_indent(
        """Parent class without last blank line.

This is parent.

Attributes
----------
name : str
    The name of
    the parent.
age
    age

Notes
-----
This is note.
""",
        'class',
    )


def test_parent_no_blank_line_func() -> None:
    assert ParentNoBlankLine.func1.__doc__ == add_indent(
        """Function 1.

Parameters
----------
a : str
    The first parameter.
    Yes, it is.
b : int
    The second parameter.
    No, it is not.
c : dict[str, int | float]
    The third parameter.
    humm...

Returns
-------
ret : tuple[str, ...]
    The return value.
""",
        'func',
    )


@inherit_docstring
class ChildNoBlankLine(ParentNoBlankLine):
    """Child class without last blank line.

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


def test_child_no_blank_line_class() -> None:
    assert ChildNoBlankLine.__doc__ == add_indent(
        """Child class without last blank line.

This is child.

Attributes
----------
name : str
    The name of
    the child.
age
    age
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


def test_child_no_blank_line_func() -> None:
    assert ChildNoBlankLine.func1.__doc__ == add_indent(
        """Function 1.

Parameters
----------
a : str
    The first parameter in child.
    Yes, it is.
b : int
    The second parameter.
    No, it is not.
c : dict[str, int | float]
    The third parameter.
    humm...

Returns
-------
ret : tuple[str, ...]
    The return value.
""",
        'func',
    )
