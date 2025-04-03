# Resumidor
Optimize text analysis by summarizing and extracting the most relevant information with the help of an LLM chat based.

# How to use

### Environment Setup

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

### Download Model
```bash
   echo "HF_TOKEN=<Your huggingface token>" > .env
   python download.py
```

### Deployment using Docker
```bash
    docker compose up -d
```

Access the app in your browser at `http://localhost:8501`.
