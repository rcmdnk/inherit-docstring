#!/usr/bin/env bash

py_ver="3.12,3.11,3.10"
py_main=${py_ver%%,*}
os="ubuntu-latest" # "ubuntu-latest, macos-latest, windows-latest"
os_main=${os%%,*}
cli="no" # "yes" or "no"

user=$(git config --get user.name)
email=$(git config --get user.email)

year=$(date +%Y)
repo_url=$(git remote get-url origin)
repo_name=$(basename -s .git "$repo_url")
repo_user=$(basename "$(dirname "$repo_url)")")
repo_name_underscore=${repo_name//-/_}

py_list=""
py_max=0
py_min=100
py_vers=""
for p in ${py_ver//,/ };do
  py_list="${py_list}          - \"$p\"\n"
  if [ -n "$py_vers" ];then
    py_vers="${py_vers}, "
  fi
  py_vers="${py_vers}\"$p\""
  ver=${p#*.}
  if (( ver > py_max ));then
    py_max=$ver
  fi
  if (( ver < py_min ));then
    py_min=$ver
  fi
done

os_list=""
for o in ${os//,/ };do
  os_list="${os_list}          - \"$o\"\n"
done

function sedi {
  local tmpfile
  tmpfile=$(mktemp)
  local cmd="$1"
  local file="$2"
  sed "$cmd" "$file" > "$tmpfile"
  mv "$tmpfile" "$file"
}

cat << EOF > README.md
# $repo_name

[![test](https://github.com/$repo_user/$repo_name/actions/workflows/test.yml/badge.svg)](https://github.com/$repo_user/$repo_name/actions/workflows/test.yml)
[![test coverage](https://img.shields.io/badge/coverage-check%20here-blue.svg)](https://github.com/$repo_user/$repo_name/tree/coverage)

...

## Requirement

- Python ${py_vers//\"/}
- Poetry (For development)

## Installation

...

## Usage

...
EOF

sedi "s|REPO_URL|$repo_url|" DEVELOPMENT.md

sedi "s|rcmdnk/python-template|$repo_user/$repo_name|" pyproject.toml
if [ -n "$user" ] && [ -n "$email" ];then
  sedi "s/USER/$user/" pyproject.toml
  sedi "s/EMAIL@example.com/$email/" pyproject.toml
fi
sedi "s/python-template/$repo_name/" pyproject.toml
sedi "s/python_template/$repo_name_underscore/" pyproject.toml
sedi "s/python = \">=3.10,<3.11\"/python = \">=3.$py_min,<3.$((py_max+1))\"/" pyproject.toml

sedi "s/\[yyyy\]/$year/" LICENSE
sedi "s/\[name of copyright owner\]/@${user}/" LICENSE

mv "src/python_template" "src/$repo_name_underscore"
sedi "s/python_template/$repo_name_underscore/" tests/test_version.py

sedi "s/default: \"3.10\"/default: \"$py_main\"/" .github/workflows/test.yml
sedi "s/          - \"3.10\"/$py_list/" .github/workflows/test.yml
sedi "s/inputs.main_py_ver || '3.10'/inputs.main_py_ver || '$py_main'/" .github/workflows/test.yml
sedi "s/python-version: \[\"3.10\"\]/python-version: \[$py_vers\]/" .github/workflows/test.yml
sedi "s/default: \"ubuntu-latest\"/default: \"$os_main\"/" .github/workflows/test.yml
sedi "s/          - \"ubuntu-latest\"/$os_list/" .github/workflows/test.yml
sedi "s/inputs.main_os || 'ubuntu-latest'/inputs.main_os || '$os_main'/" .github/workflows/test.yml
sedi "s/os: \[ubuntu-latest\]/os: \[$os\]/" .github/workflows/test.yml

if [ "$cli" = "yes" ];then
  cat << EOF >> pyproject.toml

[tool.poetry.scripts]
$repo_name = "$repo_name_underscore:main"
EOF
  cat << EOF > "src/$repo_name_underscore/${repo_name_underscore}.py"
import sys


def main() -> None:
    match len(sys.argv):
        case 1:
            print("Hello World!")
        case 2:
            print(f"Hello {sys.argv[1]}!")
        case _:
            print(f"Hello {', '.join(sys.argv[1:])}!")


if __name__ == "__main__":
    main()
EOF
  cat << EOF > "src/$repo_name_underscore/__init__.py"
from .__version__ import __version__
from .${repo_name_underscore} import main

__all__ = ["__version__", "main"]
EOF
  cat << EOF > "tests/test_${repo_name_underscore}.py"
import sys

import pytest

from $repo_name_underscore import main


@pytest.mark.parametrize(
    "argv, out",
    [
        (["$repo_name_underscore"], "Hello World!\n"),
        (["$repo_name_underscore", "Alice"], "Hello Alice!\n"),
        (
            ["$repo_name_underscore", "Alice", "Bob", "Carol"],
            "Hello Alice, Bob, Carol!\n",
        ),
    ],
)
def test_main(argv, out, capsys):
    sys.argv = argv
    main()
    captured = capsys.readouterr()
    assert captured.out == out
EOF
fi

rm -f setup.sh poetry.lock .github/workflows/template_test.yml .github/FUNDING.yml
