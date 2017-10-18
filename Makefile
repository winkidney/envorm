test:
	py.test --cov=envorm
build:
	python setup.py bdist_wheel --universal
