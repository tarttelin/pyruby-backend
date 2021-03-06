
ci: install test flake8 reqs

install:
	pipenv --python 3.10 install --dev

test:
	pipenv run pytest

flake8:
	pipenv run flake8 pyruby_backend

reqs:
	pipenv lock -r > requirements.txt