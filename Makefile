.PHONY: clean dist test docs docs-serve upload

test:
	uv run --group dev pytest

dist:
	uv build

upload:
	uv publish

docs:
	uv run --group docs mkdocs build

docs-serve:
	uv run --group docs mkdocs serve

clean:
	rm -rf dist build site .pytest_cache
	find . -type d -name '*.egg-info' -o -type d -name '__pycache__' | xargs rm -rf
