# findtools

Findtools is a pythonic implementation of file search routines inspired by GNU Findutils.


```python
from findtools.find_files import (find_files, Match)


# Recursively find all *.sh files in **/usr/bin**
sh_files_pattern = Match(filetype='f', name='*.sh')
found_files = find_files(path='/usr/bin', match=sh_files_pattern)

for found_file in found_files:
	print(found_file)
```

The above is equivalent to

```
find /usr/bin -type f -name '*.sh'
```


## Install

You can install this library by via `pip`:

<blockquote>
    pip install findtools
</blockquote>

## Develop

Alternatively you can clone this git repository. Then if you are using pyenv or miniconda as your local development setup

<blockquote>
    git clone https://github.com/ewiger/findtools.git findtools && cd findtools
    pip install -e .
</blockquote>

This will symlink you local copy and help you testign the package locally.

## Test

You can run tests yourself with built-in `unittest` lib:

    cd tests && python test_findtools.py

or with pytest:

    cd tests && pytest

Package has been tested on **python3.8+** and **python2.7+**.

Upgrade to latest with `pip install findtools==1.1.0`

Please report issues if this breaks for you.
