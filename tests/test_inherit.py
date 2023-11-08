def test_parent_class(parent):
    assert (
        parent.__doc__
        == """Parent class.

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
    )


def test_parent_func(parent):
    assert (
        parent.func1.__doc__
        == """Function 1.

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
    )


def test_child1_class(child1):
    assert (
        child1.__doc__
        == """Child class.

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
    """
    )


def test_child1_func(child1):
    assert (
        child1.func1.__doc__
        == """Function 1.

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
        """
    )


def test_child2_class(child2):
    assert (
        child2.__doc__
        == """Child 2 class.

    Attributes
    ----------
    name : str
        The name of
        the child2.
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
    """
    )


def test_child_with_conmlex_params(child3):
    assert (
        child3.__doc__
        == """Child 3 class.

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
    """
    )


def test_parent_with_colon_class(parent_with_colon):
    assert (
        parent_with_colon.__doc__
        == """Parent class.

    This is parent.

    Attributes
    ----------
    name : str
        With colon.
        X: Y
        With colon.
    """
    )


def test_child_with_colon_class(child_with_colon):
    assert (
        child_with_colon.__doc__
        == """Child class.

    Attributes
    ----------
    name : str
        With colon.
        X: Y
        With colon.
    """
    )


def test_parent_with_deprecated_class(parent_with_deprecated):
    assert (
        parent_with_deprecated.__doc__
        == """Parent class.

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


def test_child_with_deprecated_class(child_with_deprecated):
    assert (
        child_with_deprecated.__doc__
        == """Child class.

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
