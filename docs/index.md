# findtools

Findtools is a pythonic implementation of file search routines inspired by
[GNU Findutils](https://www.gnu.org/software/findutils/).

It gives you the expressiveness of the `find` command as a lazy Python
generator — match by file type and name patterns (shell wildcards or
regular expressions), and collect whatever you need from each hit.

```python
from findtools.find_files import find_files, Match

# Recursively find all *.sh files in /usr/bin
sh_files_pattern = Match(filetype='f', name='*.sh')
found_files = find_files(path='/usr/bin', match=sh_files_pattern)

for found_file in found_files:
    print(found_file)
```

The above is equivalent to:

```sh
find /usr/bin -type f -name '*.sh'
```

## Installation

```sh
pip install findtools
```

or with [uv](https://docs.astral.sh/uv/):

```sh
uv add findtools
```

Requires Python 3.10+.

## Why findtools?

- **Lazy** — `find_files()` is a generator; huge trees are streamed, not
  buffered.
- **Composable** — combine file type conditions and name patterns with
  *all* or *any* semantics.
- **Familiar** — mirrors the mental model of GNU `find`
  (`-type`, `-name`).
- **Zero dependencies** — pure standard library.

## Next steps

- Walk through the [Usage guide](usage.md) for patterns, matchers and
  collectors.
- Browse the [API Reference](api.md).
