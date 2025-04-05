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
    default="lmstudio-community/Qwen2.5-7B-Instruct-1M-GGUF",
    help="Hugging Face repo id",
)

parser.add_argument(
    "--filename",
    type=str,
    default="Qwen2.5-7B-Instruct-1M-Q4_K_M.gguf",
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
filename: str = args.filename
local_dir: str = args.local_dir

if not repo_id:
    raise ValueError("Repo ID is required. Please provide a repo ID.")

if not filename:
    raise ValueError("Filename is required. Please provide a filename.")

# Check if the model is already downloaded

logger(
    f"Checking if the file {filename} is already downloaded in {local_dir}",
    level="info",
)
login(token=os.environ.get("HF_TOKEN"))


# Download the model from Hugging Face
logger(
    f"Downloading the file {filename} from {repo_id} to {local_dir}",
    level="info",
)

file_path = hf_hub_download(
    repo_id=repo_id,
    filename=filename,
    force_download=False,
    local_files_only=False,
)

# Copy the downloaded file to the local directory
shutil.copy(file_path, os.path.join(local_dir, filename))

# Remove the original file if it exists
os.remove(file_path)

logger(
    f"File {filename} downloaded successfully to {local_dir}",
    level="info",
)
