import argparse
import os
import shutil

from huggingface_hub import login, hf_hub_download
from dotenv import load_dotenv

from loggings import logger

load_dotenv(".env.vllm")

parser = argparse.ArgumentParser(
    description="Download a model from Hugging Face and save it locally."
)

parser.add_argument(
    "--repo-id",
    type=str,
    default="Qwen/Qwen2.5-0.5B-Instruct-GGUF",
    help="Hugging Face repo id",
)

parser.add_argument(
    "--model-name",
    type=str,
    default="qwen2.5-0.5b-instruct-fp16.gguf",
    help="The name of the model to download from Hugging Face.",
)

parser.add_argument(
    "--local-dir",
    type=str,
    default="./models/",
    help="The local directory to save the downloaded model.",
)

args = parser.parse_args()

repo_id: str = args.repo_id
model_name: str = args.model_name
local_dir: str = args.local_dir

if not repo_id:
    raise ValueError("Repo ID is required. Please provide a repo ID.")

if not model_name:
    raise ValueError("Model name is required. Please provide a model name.")

# Check if the model is already downloaded

logger(
    f"Checking if the model {model_name} is already downloaded in {local_dir}",
    level="info",
)
login(token=os.environ.get("HF_TOKEN"))


# Download the model from Hugging Face
logger(
    f"Downloading the model {model_name} from {repo_id} to {local_dir}",
    level="info",
)

file_path = hf_hub_download(
    repo_id=repo_id,
    filename=model_name,
    cache_dir=local_dir,
    force_download=False,
    local_files_only=False,
)

shutil.move(file_path, os.path.join(local_dir, model_name))

logger(
    f"Model {model_name} downloaded successfully to {local_dir}",
    level="info",
)
