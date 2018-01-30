all:
	python setup.py check --restructuredtext
	python setup.py sdist bdist_wheel >/dev/null

testpypi:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi:
	twine upload dist/*

.PHONY: all
