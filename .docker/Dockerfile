ARG VARIANT=3.11
FROM python:${VARIANT}-alpine
ENV POETRY_VIRTUALENVS_CREATE=0 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml .

RUN python -m pip install --no-cache-dir --upgrade --quiet pip wheel
RUN pip install --no-cache-dir --quiet "poetry~=1.8"
RUN poetry install --no-ansi --without dev

COPY loterias/ /fastapi-loterias-api
COPY .env .

CMD ["poetry","run","fastapi","run","/fastapi-loterias-api/main.py"]
