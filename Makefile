init:
	pip install pipenv coveralls
	pipenv install --dev

test:
	pipenv run coverage run manage.py test posts --failfast --settings=blog.settings.test && coverage report