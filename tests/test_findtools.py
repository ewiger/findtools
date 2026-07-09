import os
import re

import pytest

from findtools.core import change_dir, touch
from findtools.find_files import (
    Match,
    MatchAllPatternsAndTypes,
    MatchAnyPatternsAndTypes,
    collect_size,
    find_files,
)


@pytest.fixture
def tree(tmp_path):
    '''A directory tree with empty dirs, empty files and non-empty files.

    tmp_path/
        0/ .. 9/                    (empty directories)
        with_files/0 .. 11          (empty files)
        diff_files/0 .. 11          (files of increasing size)
    '''
    for num in range(10):
        (tmp_path / str(num)).mkdir()
    with_files = tmp_path / 'with_files'
    with_files.mkdir()
    for num in range(12):
        touch(str(with_files / str(num)))
    diff_files = tmp_path / 'diff_files'
    diff_files.mkdir()
    for num in range(12):
        (diff_files / str(num)).write_text(
            ''.join(str(ch) for ch in range(num)))
    return tmp_path


def test_find_everything(tree):
    pathnames = list(find_files(str(tree)))
    # 10 empty dirs + 2 dirs + 24 files.
    assert len(pathnames) == 36


def test_find_by_filetype(tree):
    with_files = str(tree / 'with_files')
    assert list(find_files(with_files, Match(filetype='d'))) == []
    assert len(list(find_files(with_files, Match(filetype='f')))) == 12


def test_find_by_fnmatch_pattern(tree):
    with_files = str(tree / 'with_files')
    found = list(find_files(with_files, Match(filetype='f', name='1*')))
    # '1', '10', '11'
    assert len(found) == 3
    assert all(os.path.basename(pn).startswith('1') for pn in found)


def test_find_by_name_only(tree):
    # Match with a name but no filetype must work and match dirs too.
    found = list(find_files(str(tree), Match(name='4')))
    basenames = [os.path.basename(pn) for pn in found]
    # dir '4', file 'with_files/4', file 'diff_files/4'
    assert basenames.count('4') == 3


def test_match_requires_an_argument():
    with pytest.raises(ValueError):
        Match()


def test_find_by_regexp_string(tree):
    # A string wrapped in slashes is interpreted as a regexp.
    with_files = str(tree / 'with_files')
    found = list(find_files(with_files, Match(filetype='f', name=r'/1\d/')))
    assert sorted(os.path.basename(pn) for pn in found) == ['10', '11']


def test_find_by_precompiled_regexp(tree):
    # Regression: pre-compiled regexps in `names` used to be silently
    # dropped, matching everything.
    with_files = str(tree / 'with_files')
    matcher = MatchAllPatternsAndTypes(names=[re.compile(r'1\d$')])
    found = list(find_files(with_files, matcher))
    assert sorted(os.path.basename(pn) for pn in found) == ['10', '11']


def test_find_non_recursive(tree):
    found = list(find_files(str(tree), recursive=False))
    # Only the 12 top-level directories, none of the nested files.
    assert len(found) == 12
    assert all(os.path.isdir(pn) for pn in found)


def test_find_non_recursive_on_a_file(tree):
    # Regression: used to raise a raw StopIteration.
    a_file = str(tree / 'with_files' / '0')
    assert list(find_files(a_file, recursive=False)) == []


def test_find_missing_path_raises(tree):
    with pytest.raises(FileNotFoundError):
        list(find_files(str(tree / 'no_such_dir')))


def test_collect_size(tree):
    file_search = find_files(
        str(tree / 'diff_files'),
        Match(filetype='f', name='1*'),
        collect_size,
    )
    sizes = dict(file_search)
    assert len(sizes) == 3
    assert all(size > 0 for size in sizes.values())


def test_match_any_of_patterns_and_types(tree):
    with_files = tree / 'with_files'
    for num in range(20, 30):
        (with_files / str(num)).mkdir()
    file_search = find_files(
        str(with_files),
        MatchAnyPatternsAndTypes(filetypes=['f', 'd'], names=['*4']),
    )
    basenames = sorted(os.path.basename(pn) for pn in file_search)
    assert basenames == ['24', '4']


def test_match_all_patterns_and_types(tree):
    file_search = find_files(
        str(tree / 'with_files'),
        MatchAllPatternsAndTypes(filetypes=['f'], names=['1*', '*1']),
    )
    basenames = sorted(os.path.basename(pn) for pn in file_search)
    # Must match both patterns: starts with 1 AND ends with 1.
    assert basenames == ['1', '11']


def test_find_symlinks(tree):
    target = tree / 'with_files' / '0'
    link = tree / 'with_files' / 'link_to_0'
    os.symlink(str(target), str(link))
    found = list(
        find_files(str(tree / 'with_files'), Match(filetype='l')))
    assert [os.path.basename(pn) for pn in found] == ['link_to_0']


def test_touch_creates_file(tmp_path):
    filename = str(tmp_path / 'touched')
    touch(filename)
    assert os.path.isfile(filename)


def test_change_dir(tmp_path):
    original = os.getcwd()
    with change_dir(str(tmp_path)):
        assert os.getcwd() == os.path.realpath(str(tmp_path))
    assert os.getcwd() == original
