from huggingface_hub import snapshot_download
import joblib

REPO_ID = "meta-llama/Llama-2-7b-chat"
FILENAME = "sklearn_model.joblib"

model = joblib.load(
    snapshot_download(repo_id=REPO_ID)
)