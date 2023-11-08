import pytest

from inherit_docstring import inherit_docstring


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


@inherit_docstring
class Child1(Parent):
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


@inherit_docstring
class Child2(Child1):
    """Child 2 class.

    Attributes
    ----------
    name : str
        The name of
        the child2.
    c_int : int
        The int value.
    """


@pytest.fixture
def parent():
    return Parent()


@pytest.fixture
def child1():
    return Child1()


@pytest.fixture
def child2():
    return Child2()


@inherit_docstring
class Child3(Parent):
    """Child 3 class.

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
    """  # noqa: RST301, RST201, RST213, RST210


@pytest.fixture
def child3():
    return Child3()


class ParentWithColon:
    """Parent class.

    This is parent.

    Attributes
    ----------
    name : str
        With colon.
        X: Y
        With colon.
    """


@inherit_docstring
class ChildWithColon(ParentWithColon):
    """Child class."""


@pytest.fixture
def parent_with_colon():
    return ParentWithColon()


@pytest.fixture
def child_with_colon():
    return ChildWithColon()


class ParentWithDeprecated:
    """Parent class.

    This is parent.

    Attributes
    ----------
    name : str
        The name of
        the parent.
    age
        age

    .. deprecated:: 0.1.0
        Deprecated.
        0.1.0.
    """  # noqa: RST303


@inherit_docstring
class ChildWithDeprecated(ParentWithDeprecated):
    """Child class.

    .. deprecated:: 0.2.0
        Deprecated.
        0.2.0.
    """  # noqa: RST303


@pytest.fixture
def parent_with_deprecated():
    return ParentWithDeprecated()


@pytest.fixture
def child_with_deprecated():
    return ChildWithDeprecated()
