test:
	pytest -v

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

dev:
	gulp --cwd slackforms/staticapp/

database:
	dropdb slackforms --if-exists
	createdb slackforms
