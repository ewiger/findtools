# findtools

[![CI](https://github.com/ewiger/findtools/actions/workflows/ci.yml/badge.svg)](https://github.com/ewiger/findtools/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/findtools)](https://pypi.org/project/findtools/)

Findtools is a pythonic implementation of file search routines inspired by
GNU Findutils.

**Documentation: <https://ewiger.github.io/findtools/>**

```python
from findtools.find_files import find_files, Match


# Recursively find all *.sh files in /usr/bin
sh_files_pattern = Match(filetype='f', name='*.sh')
found_files = find_files(path='/usr/bin', match=sh_files_pattern)

for found_file in found_files:
    print(found_file)
```

The above is equivalent to

```sh
find /usr/bin -type f -name '*.sh'
```

## Install

```sh
pip install findtools
```

or with [uv](https://docs.astral.sh/uv/):

```sh
uv add findtools
```

Requires Python 3.9+. Findtools has no dependencies outside the standard
library.

## Develop

The project is managed with [uv](https://docs.astral.sh/uv/):

```sh
git clone https://github.com/ewiger/findtools.git && cd findtools
uv sync --group dev
```

## Test

Run the test suite with pytest:

```sh
uv run pytest
```

or via make:

```sh
make test
```

## Documentation

The docs are built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
and deployed to GitHub Pages on every push to `master`. To preview locally:

```sh
make docs-serve
```

Please report issues at <https://github.com/ewiger/findtools/issues>.
