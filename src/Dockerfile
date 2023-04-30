ARG PYTHON_VERSION=3.10.4

FROM python:${PYTHON_VERSION}-slim-buster

ARG APP_ROOT=/code
ARG APP_USER=web

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry
    POETRY_VERSION=1.3.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/var/cache/pypoetry \
    POETRY_HOME=/usr/local \
    # Dockerize
    DOCKERIZE_VERSION=v0.6.1


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
      bash \
      curl \
      wget \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    # Installing `dockerize` utility:
    # https://github.com/jwilder/dockerize
    && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && dockerize --version \
    # Installing setuptools:
    # https://github.com/pypa/setuptools/issues/581
    && wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python

WORKDIR ${APP_ROOT}

RUN groupadd -r ${APP_USER} \
     && useradd -d ${APP_ROOT} -r -g ${APP_USER} ${APP_USER} \
     && chown ${APP_USER}:${APP_USER} -R ${APP_ROOT}

COPY poetry.lock pyproject.toml ${APP_ROOT}/

RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
    poetry install --no-interaction --no-ansi \
    && pip install setuptools

COPY ./src ${APP_ROOT}

USER ${APP_USER}

CMD ["python3", "main.py"]