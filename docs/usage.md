# Usage

## Basic search

`find_files()` walks a directory tree and yields matching pathnames:

```python
from findtools.find_files import find_files, Match

for pathname in find_files('/var/log', Match(filetype='f', name='*.log')):
    print(pathname)
```

Without a matcher, every file and directory in the tree is yielded:

```python
everything = list(find_files('/etc'))
```

## File types

`Match(filetype=...)` accepts the same single-letter flags as
`find -type`, or their long names:

| Flag | Long name    | Matches            |
|------|--------------|--------------------|
| `f`  | `file`       | regular files      |
| `d`  | `directory`  | directories        |
| `l`  | `link`       | symbolic links     |

```python
directories = find_files('/tmp', Match(filetype='d'))
symlinks = find_files('/usr/local/bin', Match(filetype='l'))
```

## Name patterns

Three kinds of name patterns are understood:

```python
# 1. Shell wildcard (fnmatch) — like find -name
Match(name='*.tar.gz')

# 2. Regular expression as a /slash-wrapped/ string
Match(name=r'/\d{4}-\d{2}-\d{2}\.log/')

# 3. A pre-compiled regular expression object
import re
from findtools.find_files import MatchAllPatternsAndTypes
MatchAllPatternsAndTypes(names=[re.compile(r'backup_\d+')])
```

!!! note
    Patterns are matched against the *basename* of each entry, not the
    full path — the same as `find -name`.

## Combining conditions: all vs any

`MatchAllPatternsAndTypes` requires **every** condition to hold,
`MatchAnyPatternsAndTypes` is satisfied by **any** of them:

```python
from findtools.find_files import (
    find_files,
    MatchAllPatternsAndTypes,
    MatchAnyPatternsAndTypes,
)

# Files whose name starts with "1" AND ends with "1"
strict = MatchAllPatternsAndTypes(filetypes=['f'], names=['1*', '*1'])

# Anything that is a file OR a directory, named "*.bak" OR "*.tmp"
loose = MatchAnyPatternsAndTypes(
    filetypes=['f', 'd'],
    names=['*.bak', '*.tmp'],
)

stale = find_files('/var/cache', loose)
```

`Match` is a convenience shortcut for a single filetype and/or a single
name pattern with *all* semantics.

## Collectors

By default each match yields its full pathname. Pass a different
`collect` callable to shape the results — for example, the bundled
`collect_size`:

```python
from findtools.find_files import find_files, Match, collect_size

for pathname, size in find_files('/var/log',
                                 Match(filetype='f', name='*.log'),
                                 collect=collect_size):
    print('%s: %d bytes' % (pathname, size))
```

A collector is any callable `(root, name) -> result`:

```python
import os

def collect_mtime(root, name):
    pathname = os.path.join(root, name)
    return pathname, os.path.getmtime(pathname)
```

## Non-recursive search

Limit the search to the top level of a directory, like
`find -maxdepth 1`:

```python
top_level_only = find_files('/opt', Match(filetype='d'), recursive=False)
```

## Helpers in `findtools.core`

```python
from findtools.core import touch, change_dir

# Create an empty file / update its timestamps, like the touch command
touch('/tmp/marker')

# Temporarily change the working directory
with change_dir('/tmp', 'build'):
    ...  # cwd is /tmp/build here
# cwd is restored afterwards
```
