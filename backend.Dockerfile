FROM python:3.13-slim-bullseye

WORKDIR /app

COPY pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root


COPY . .

EXPOSE 3000

CMD ["poetry", "run", "fastapi", "run", "server/main.py", "--port", "3000", "--host", "0.0.0.0"]
