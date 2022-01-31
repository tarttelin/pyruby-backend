
ci: install test flake8 reqs

install:
	pipenv install --dev

test:
	pipenv run pytest

flake8:
	pipenv run flake8 pyruby_backend

reqs:
	pipenv run pip freeze > requirements.txt