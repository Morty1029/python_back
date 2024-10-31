
FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app


CMD ["poetry", "run", "uvicorn", "shop_api.main:app", "--host", "0.0.0.0", "--port", "8080"]