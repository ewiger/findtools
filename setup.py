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


setup(
    name='findtools',
    version='1.0.0',
    description='Python implementation of GNU Findutils',
    long_description=readme(),
    author='Yauhen Yakimovich',
    author_email='eugeny.yakimovitch@gmail.com',
    url='https://github.com/ewiger/findtools',
    license='GPL',
    scripts=glob('bin/*'),
    #data_files=glob('libexec/*'),
    packages=['findtools'],
    package_dir={
        'findtools': 'src/findtools',
    },
    download_url='https://github.com/ewiger/findtools/tarball/master',
    install_requires=[
        'sh >= 1.08',
        'daemoncxt >= 1.5.7',
    ],
)
