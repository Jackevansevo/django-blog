ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim

ARG DJANGO_SETTINGS_MODULE=blog.settings.dev
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE}

ARG SENTRY_DSN
ENV SENTRY_DSN ${SENTRY_DSN}

RUN apt-get update && apt-get install

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "blog.wsgi"]
