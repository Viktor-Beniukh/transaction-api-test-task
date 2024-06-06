FROM python:3.11 as requirements-stage

WORKDIR /tmp


RUN pip install poetry


COPY ./pyproject.toml ./poetry.lock* /tmp/


RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc


RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


COPY . /code/


RUN adduser \
    --disabled-password \
    --no-create-home \
    django-user

RUN chown -R django-user:django-user /code/
RUN chmod -R 755 /code/

USER django-user
