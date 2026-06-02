import sys
from pathlib import Path

import pytest
from git import Repo
from git.exc import InvalidGitRepositoryError

from inherit_docstring import __version__

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def test_version() -> None:
    with (Path(__file__).parents[1] / 'pyproject.toml').open('rb') as f:
        version = tomllib.load(f)['project']['version']
    assert version == __version__


def test_tag() -> None:
    try:
        repo = Repo(Path(__file__).parents[1])
    except InvalidGitRepositoryError:
        pytest.skip('Not a git repo.')
    tags = repo.git.tag(sort='creatordate').splitlines()
    if len(tags) > 0:
        latest_tag = tags[-1]
        assert latest_tag == 'v' + __version__
