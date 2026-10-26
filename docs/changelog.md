# Changelog

## Unreleased

### Changed

- Dropped Python 3.9 support (end of life since October 2025); requires
  Python 3.10+.

## 1.2.0 (2026-07-09)

Revitalization release.

### Fixed

- Pre-compiled regular expressions passed in `names` to
  `MatchAllPatternsAndTypes` / `MatchAnyPatternsAndTypes` were silently
  ignored (assigned to a dead attribute), causing the matcher to accept
  every name.
- `find_files(path, recursive=False)` raised a raw `StopIteration` when
  `path` pointed to a file instead of a directory; it now yields no
  results.
- `find_files` raises `FileNotFoundError` (instead of a bare
  `Exception`) for missing paths.
- `Match()` with neither `filetype` nor `name` raises `ValueError`
  (instead of a bare `Exception`); `Match(name=...)` no longer
  constructs a useless always-true file type condition.

### Changed

- Dropped Python 2.7 support; requires Python 3.9+.
- Modern packaging: `pyproject.toml` replaces `setup.py`; development
  workflow uses [uv](https://docs.astral.sh/uv/).
- Test suite migrated to pytest with regression coverage for all fixes.
- New documentation site built with Material for MkDocs.

## 1.1.0 (2020-07-30)

- Updated for Python 3.8 while keeping Python 2.7 compatibility.
- Packaging updates.

## 1.0.x (2014)

- Initial public releases: `find_files`, `Match`,
  `MatchAllPatternsAndTypes`, `MatchAnyPatternsAndTypes`,
  `collect_size`, core helpers `touch` and `change_dir`.
