from __future__ import annotations

from inherit_docstring import inherit_docstring

from .utils import add_indent


class Parent:
    """Parent class.

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


def test_parent_class() -> None:
    assert Parent.__doc__ == add_indent(
        """Parent class.

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


def test_parent_func() -> None:
    assert Parent.func1.__doc__ == add_indent(
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
class Child(Parent):
    """Child class.

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


def test_child_class() -> None:
    assert Child.__doc__ == add_indent(
        """Child class.

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


def test_child_func() -> None:
    assert Child.func1.__doc__ == add_indent(
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


@inherit_docstring
class Decendant(Child):
    """Decendant class.

    Attributes
    ----------
    name : str
        The name of
        the decendant.
    c_int : int
        The int value.

    """


def test_decendant_class() -> None:
    assert Decendant.__doc__ == add_indent(
        """Decendant class.

Attributes
----------
name : str
    The name of
    the decendant.
age
    age
child_attr : int
    The child attribute.
c_int : int
    The int value.

Notes
-----
This is child note.

Examples
--------
This is example.

""",
        'class',
    )


@inherit_docstring
class ComplicatedParamsChild(Parent):
    """Child class with complicated parameters.

    Attributes
    ----------
    x : int, optional
    copy1 : bool, default True
    copy2 : bool, default=True
    copy3 : bool, default: True
    order : {'C', 'F', 'A'}
        Description of `order`.
    x1, x2 : array_like
        Input arrays, description of `x1`, `x2`.
    *args : tuple
        Additional arguments should be passed as keyword arguments
    **kwargs : dict, optional
        Extra arguments to `metric`: refer to each metric documentation for a
        list of all possible arguments.

    """


def test_child_with_conmlex_params() -> None:
    assert ComplicatedParamsChild.__doc__ == add_indent(
        """Child class with complicated parameters.

Attributes
----------
name : str
    The name of
    the parent.
age
    age
x : int, optional
copy1 : bool, default True
copy2 : bool, default=True
copy3 : bool, default: True
order : {'C', 'F', 'A'}
    Description of `order`.
x1, x2 : array_like
    Input arrays, description of `x1`, `x2`.
*args : tuple
    Additional arguments should be passed as keyword arguments
**kwargs : dict, optional
    Extra arguments to `metric`: refer to each metric documentation for a
    list of all possible arguments.

Notes
-----
This is note.

""",
        'class',
    )
