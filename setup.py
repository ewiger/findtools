#!/usr/bin/env python
"""

`python3 -m pip install --user --upgrade setuptools wheel twine`

Required:
    setuptools >= 38.6.0
    wheel >= 0.31.0
    twine >= 1.11.0

`python setup.py bdist_egg`
`twine check dist/*`
`twine upload dist/*`
"""
import os.path
import sys
from glob import glob

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


def get_version():
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path = [src_path] + sys.path
    import findtools
    findtools.__path__
    return findtools.__version__


setup(
    name='findtools',
    version=get_version(),
    description='Python implementation of GNU Findutils',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Yauhen Yakimovich',
    author_email='eugeny.yakimovitch@gmail.com',
    url='https://github.com/ewiger/findtools',
    license='GPL',
    #scripts=glob('bin/*'),
    #data_files=glob('libexec/*'),
    packages=['findtools'],
    package_dir={
        'findtools': 'src/findtools',
    },
    download_url='https://github.com/ewiger/findtools/tarball/master',
)
