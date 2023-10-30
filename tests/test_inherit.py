def test_parent_class(parent):
    assert (
        parent.__doc__
        == """Parent class.

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
    )


def test_parent_func(parent):
    assert (
        parent.func1.__doc__
        == """Function 1.

        Parameters
        ----------
        a: str
            The first parameter.
            Yes, it is.
        b: int
            The second parameter.
            No, it is not.
        c: dict[str, int]
            The third parameter.
            humm...

        Returns
        -------
        ret: int
            The return value.
        """
    )


def test_child1_class(child1):
    assert (
        child1.__doc__
        == """Child class.

    This is child.

    Attributes
    ----------
    name: str
        The name of
        the child.
    age:
        age
    child_attr: int
        The child attribute.

    Returns
    -------
    ret: int
        The return value.

    Notes
    -----
    This is child note.

    Examples
    --------
    This is example.
    """
    )


def test_child1_func(child1):
    assert (
        child1.func1.__doc__
        == """Function 1.

        Parameters
        ----------
        a: str
            The first parameter in child.
            Yes, it is.
        b: int
            The second parameter.
            No, it is not.
        c: dict[str, int]
            The third parameter.
            humm...

        Returns
        -------
        ret: int
            The return value.
        """
    )


def test_child2_class(child2):
    assert (
        child2.__doc__
        == """Child 2 class.

    Attributes
    ----------
    name: str
        The name of
        the child2.
    age:
        age
    child_attr: int
        The child attribute.
    c_int: int
        The int value.

    Returns
    -------
    ret: int
        The return value.

    Notes
    -----
    This is child note.

    Examples
    --------
    This is example.
    """
    )


def test_parent_with_colon_class(parent_with_colon):
    assert (
        parent_with_colon.__doc__
        == """Parent class.

    This is parent.

    Attributes
    ----------
    name: str
        With colon.
        X: Y
        With colon.
    """
    )


def test_child_with_colon_class(child_with_colon):
    # TODO: fix this
    # Currently if ':' is in the comment, it is not parsed correctly.
    # X: Y should be the comment of the name.
    assert (
        child_with_colon.__doc__
        == """Child class.

    Attributes
    ----------
    name: str
        With colon.
    X: Y
        With colon.
    """
    )
