#!/usr/bin/env python
# TODO: migrate to distribute?
#import distribute_setup
#distribute_setup.use_setuptools()


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
