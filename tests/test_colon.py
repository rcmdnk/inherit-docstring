from __future__ import annotations

from inherit_docstring import inherit_docstring


class ParentWithColon:
    """Parent class with colon in descriptions.

    This is parent.

    Attributes
    ----------
    name : str
        With colon.
        X: Y
        With colon.

    """


def test_parent_with_colon_class() -> None:
    assert (
        ParentWithColon.__doc__
        == """Parent class with colon in descriptions.

    This is parent.

    Attributes
    ----------
    name : str
        With colon.
        X: Y
        With colon.

    """
    )


@inherit_docstring
class ChildWithColon(ParentWithColon):
    """Child class."""


def test_child_with_colon_class() -> None:
    assert (
        ChildWithColon.__doc__
        == """Child class.

    Attributes
    ----------
    name : str
        With colon.
        X: Y
        With colon.

    """
    )
