from __future__ import annotations

from inherit_docstring import inherit_docstring


class ParentWithDeprecated:
    """Parent class with deprecated attributes.

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

    """


def test_parent_with_deprecated_class() -> None:
    assert (
        ParentWithDeprecated.__doc__
        == """Parent class with deprecated attributes.

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

    """
    )


@inherit_docstring
class ChildWithDeprecated(ParentWithDeprecated):
    """Child class with deprecated attributes.

    .. deprecated:: 0.2.0
        Deprecated.
        0.2.0.
    """


def test_child_with_deprecated_class() -> None:
    assert (
        ChildWithDeprecated.__doc__
        == """Child class with deprecated attributes.

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

    .. deprecated:: 0.2.0
        Deprecated.
        0.2.0.

    """
    )
