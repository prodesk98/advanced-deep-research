FROM python:3.13-slim-bullseye

WORKDIR /app

COPY ../pyproject.toml ./

RUN apt-get update && apt-get install -y build-essential

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

# Install Playwright dependencies
RUN poetry run playwright install-deps firefox

COPY .. .

EXPOSE 3000

CMD ["poetry", "run", "fastapi", "run", "server/main.py", "--port", "3000", "--host", "0.0.0.0"]
