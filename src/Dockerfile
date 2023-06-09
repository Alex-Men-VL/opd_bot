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
    && poetry --version

WORKDIR ${APP_ROOT}

RUN groupadd -r ${APP_USER} \
     && useradd -d ${APP_ROOT} -r -g ${APP_USER} ${APP_USER} \
     && chown ${APP_USER}:${APP_USER} -R ${APP_ROOT}

COPY poetry.lock pyproject.toml ${APP_ROOT}/

RUN poetry config virtualenvs.create false \
    && poetry install

COPY ./src ${APP_ROOT}

USER ${APP_USER}

CMD ["python3", "/code/main.py"]