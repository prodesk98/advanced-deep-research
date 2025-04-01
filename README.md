# Resumidor
Otimize a análise de textos resumindo e extraindo as informações mais relevantes com o auxílio de um chat LLM baseado na API OpenAI.

# How to use
1. Copy the `.env.example` file to `.env` and fill in your OpenAI API key.
    ```bash
    cp .env.example .env
    ```

2. Install the required packages.
    ```bash
    pip install poetry
    poetry install
    ```
   
3. Run the script.
    ```bash
    poetry run streamlit run app.py
    ```
   
# Deployment using Docker

1. Build the Docker image.
    ```bash
    docker build -t resumidor .
    ```
   
2. Run the Docker container.
    ```bash
    docker run -p 8501:8501 --env-file .env resumidor
    ```
   
3. Access the app in your browser at `http://localhost:8501`.