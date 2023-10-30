import pytest

from inherit_docstring import inherit_docstring


class Parent:
    """Parent class.

    This is parent.

    Attributes
    ----------
    name: str
        The name of
        the parent.
    age:
        age

    Returns
    -------
    ret: int
        The return value.

    Notes
    -----
    This is note.
    """

    def func1(self, a: str, b: int, c: float) -> int:
        """Function 1.

        Parameters
        ----------
        a: str
            The first parameter.
            Yes, it is.
        b: int
            The second parameter.
            No, it is not.
        c: dict[str, int | float]
            The third parameter.
            humm...

        Returns
        -------
        ret: int
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
    child_attr: int
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
        a: str
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
    c_int: int
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


class ParentWithColon:
    """Parent class.

    This is parent.

    Attributes
    ----------
    name: str
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
