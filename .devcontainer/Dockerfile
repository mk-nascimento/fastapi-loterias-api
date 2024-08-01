ARG VARIANT=3.11
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_PROMPT=(\ py-{python_version}\ )

RUN pipx install "poetry==1.8.*"