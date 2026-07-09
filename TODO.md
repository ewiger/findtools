# findtools — Revitalization Plan

Dormant since 2020 (v1.1.0). Goal: fix known bugs, modernize tooling around
**uv** and **pytest**, and publish HTML documentation to GitHub Pages with
**Material for MkDocs** (same setup as <https://ewiger.github.io/len/>).

## Phase 1 — Bug fixes

- [x] `MatchAllPatternsAndTypes.__init__`: pre-compiled regexps passed in
      `names` are assigned to `self.name_pattern` (typo, never read) and
      silently ignored — append to `self.name_patterns` instead.
- [x] `MatchAllPatternsAndTypes.__init__`: dead name-mangled attributes
      (`self.__pathname` vs `self._pathname` used by `matches()`).
- [x] `find_files(recursive=False)`: raw `StopIteration` when `path` is a
      file — return no matches instead of crashing.
- [x] `find_files`: raise `FileNotFoundError` instead of bare `Exception`;
      fix "does not exists" grammar.
- [x] `Match(name=...)` without filetype: stop constructing a useless
      `FileTypeCondition(None)`; raise `ValueError` when both args missing.

## Phase 2 — Modern tooling (uv + pytest)

- [x] Add `pyproject.toml`: setuptools backend, src layout, dynamic version
      from `findtools.__version__`, `requires-python >= 3.9`,
      dev dependency group (`pytest`), docs group (`mkdocs-material`,
      `mkdocstrings[python]`).
- [x] Remove `setup.py` (version-import hack no longer needed).
- [x] Migrate `tests/` to pytest style; add regression tests for every
      Phase 1 fix plus: `/regexp/` string syntax, non-recursive search,
      `MatchAllPatternsAndTypes`, symlink filetype, `collect_size`,
      `core.touch` / `core.change_dir`.
- [x] Update `Makefile` to thin uv wrappers: `test`, `dist`, `docs`,
      `docs-serve`, `clean`.
- [x] Drop Python 2.7 support claims; target 3.9+.

## Phase 3 — Documentation (Material for MkDocs → GitHub Pages)

- [x] `mkdocs.yml` with Material theme, nav: Home / Usage / API Reference /
      Changelog.
- [x] `docs/` pages: index (install + quickstart), usage (patterns, types,
      collectors, recursion), API reference via mkdocstrings, changelog.
- [x] GitHub Actions workflow to build and deploy docs to `gh-pages` on
      push to `master` → serves at <https://ewiger.github.io/findtools/>.
- [x] Rewrite `README.md`: link to docs site, uv-based dev instructions,
      pytest instructions.

## Phase 4 — CI & release

- [x] GitHub Actions CI: pytest matrix (3.9–3.14) via uv.
- [x] Add `CHANGELOG.md`.
- [x] Bump version to `1.2.0`.
- [ ] Publish to PyPI (`uv build` + `uv publish`; consider PyPI trusted
      publishing from CI later).
- [ ] Enable GitHub Pages (Settings → Pages → deploy from `gh-pages`
      branch) after first docs deploy — manual, one-time.