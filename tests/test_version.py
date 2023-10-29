from pathlib import Path

import pytest
from git import Repo
from git.exc import InvalidGitRepositoryError

from python_template import __version__


def test_version():
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

    with open(Path(__file__).parents[1] / "pyproject.toml", "rb") as f:
        version = tomllib.load(f)["tool"]["poetry"]["version"]
    assert version == __version__


def test_tag():
    try:
        repo = Repo(Path(__file__).parents[1])
    except InvalidGitRepositoryError:
        pytest.skip("Not a git repo.")
    latest_tag = repo.git.tag(sort="creatordate").splitlines()[-1]
    assert latest_tag == "v" + __version__
