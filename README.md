# Simple Django Blog

[![Coverage Status](https://coveralls.io/repos/github/Jackevansevo/django-blog/badge.svg?branch=master)](https://coveralls.io/github/Jackevansevo/django-blog?branch=master)

## Features
* Code syntax highlighting (with Pygments)
* RSS support
* Post archive
* Tags
* Search

# Installation

Using [pipenv](https://github.com/pypa/pipenv)

    pipenv install --dev

Tell Django which settings file to use

    export DJANGO_SETTINGS_MODULE=blog.settings.dev

Initialize the database

    ./manage.py makemigrations posts

    ./manage.py migrate

# Local Development

## Runserver

    ./manage.py runserver

## Running a test database

    ./manage.py testserver fixtures/db.json

# Running Tests

All Django tests can be ran with the following:

    ./manage.py test posts --settings=blog.settings.test

You may wish to pass some additional flags:

    ./manage.py test posts --failfast --settings=blog.settings.test

## Test Coverage

A coverage report can be generated with the following command:

    coverage run manage.py test posts --settings=blog.settings.test && coverage report

# Screenshot

![blog screenshot](screenshot.png)
