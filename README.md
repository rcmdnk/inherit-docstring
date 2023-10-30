# inherit-docstring

[![test](https://github.com/rcmdnk/inherit-docstring/actions/workflows/test.yml/badge.svg)](https://github.com/rcmdnk/inherit-docstring/actions/workflows/test.yml)
[![test coverage](https://img.shields.io/badge/coverage-check%20here-blue.svg)](https://github.com/rcmdnk/inherit-docstring/tree/coverage)

A python decorator to inherit docstring.

Easily inherit docstrings from parent classes with `@inherit_docstring` decorator, designed specifically for [the NumPy docstring style](https://numpydoc.readthedocs.io/en/latest/format.html).

Use inherit-docstring to streamline your documentation process, ensuring consistency and reducing redundancy!

## Features

* Automatic Inheritance: Just add the `@inherit_docstring` decorator, and the child class will seamlessly inherit the parent's class and function docstrings.
* Structured Sections: Docstrings are broken into sections like `Attributes`, `Notes`, etc. Each section is denoted by its title followed by `---`.
* Header Section: An exclusive `Header` section is introduced for the starting portion of the docstring without a specific title.
* Parameter Sections: Certain sections are treated as parameter sections where the content is interpreted as parameter explanations. They include:
  * Attributes
  * Parameters
  * Returns
  * Yields
  * Receives
  * Raises
  * Warns
  * Warnings

## Behavior

* If a child class function lacks a docstring, it inherits the parent's docstring verbatim.
* For functions where both parent and child have docstrings:
    * Section-wise Merge: Docstrings are combined on a section-by-section basis.
    * Parameter-wise Merge: Within parameter sections, docstrings are combined parameter by parameter.
    * Child Priority: When both parent and child provide docstrings for the same function or parameter, the child's version is prioritized.

## Requirement

- Python 3.12, 3.11, 3.10, 3.9
- Poetry (For development)

## Installation

By pip:

```
$ pip3 install inherit-docstring
```

## Usage

Add `inherit_docstring` decorator to the inherited class:

```
from inherit_docstring import inherit_docstring

class Parent:
    """Parent class.

    This is an explanation.

    Attributes
    ----------
    name: str
        The name of
        the parent.
    age:
        The age. w/o type.

    Notes
    -----
    This is parent's note.
    """

    name: str = 'parent'
    age: int = 40

    def func1(self, param1: int, param2: int) -> int:
        """Parent's func1.

        Parameters
        ----------
        param1: int
            First input.
        param2: int
            Second input.

        Returns
        -------
        ret: int
            param1 + param2
        """

        return param1 + param2

    def func2(self) -> None:
        """Parent's func2.

        Returns
        -------
        ret: str
            something
        """

        return 'Something'

@inherit_docstring
class Child(Parent):
    """Child class.

    Attributes
    ----------
    sex: str
        Additional attributes.
        girl or boy.
    """

    sex: str = "boy"

    def func1(self, param1: int, param2: int) -> int:
        """Child's func1.

        Returns
        -------
        ret: int
            param1 - param2
        """

        return param1 - param2
```

Child class' help will be:

```
class Child(Parent)
 |  Child class.
 |
 |  Attributes
 |  ----------
 |  name: str
 |      The name of
 |      the parent.
 |  age:
 |      The age. w/o type.
 |  sex: str
 |      Additional attributes.
 |      girl or boy.
 |
 |  Notes
 |  -----
 |  This is parent's note.
 |
 |  Method resolution order:
 |      Child
 |      Parent
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  func1(self, param1: int, param2: int) -> int
 |      Child's func1.
 |
 |      Parameters
 |      ----------
 |      param1: int
 |          First input.
 |      param2: int
 |          Second input.
 |
 |      Returns
 |      -------
 |      ret: int
 |          param1 - param2
 ```



