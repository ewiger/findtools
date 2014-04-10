findtools
=========

Findtools is a pythonic implementation of file search routines inspired by
GNU Findutils.


```python
from findtools.find_files import (find_files, Match)


# Recursively find all *.sh files in **/usr/bin**
sh_files_pattern = Match(filetype='f', name='*.sh')
found_files = find_files(path='/usr/bin', match=sh_files_pattern)

for found_file in found_files:
	print found_file
```

The above is equivalent to

<blockquote>
	find /usr/bin -type f -name '*.sh'
</blockquote>



Installation
------------
You can install th library by using PyPI registry, e.g.

<blockquote>
    pip install findtools
</blockquote>

Alternatively you can clone git repository

<blockquote>
    git clone https://github.com/ewiger/findtools.git findtools && cd findtools
    sudo python setup.py install
</blockquote>

