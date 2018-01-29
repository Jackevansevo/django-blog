# Useful commands

## Running a test database

```
python manage.py testserver fixtures/db.json
```

## Loading a database snapshot

```
python manage.py loaddata fixtures/db.json
```

## Recording a Database Snapshot

```
env/bin/python manage.py dumpdata --indent=2 --exclude auth.permission --exclude contenttypes > fixtures/db.json
```

## Running tests

```
python manage.py test posts --failfast
```

### Test Coverage

```
coverage run manage.py test posts; and coverage report
```
