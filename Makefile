.PHONY: clean dist test

clean:
		rm -rf dist build *.egg-info
		find ./ -type d -name '*.egg-info' | xargs rm -rf

dist:
		python setup.py bdist_egg
		twine check dist/*

test:
		cd tests && python test_findtools.py

upload:
		twine upload dist/*
