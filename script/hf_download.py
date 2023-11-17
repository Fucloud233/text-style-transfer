from huggingface_hub import hf_hub_download, snapshot_download

# https://huggingface.co/edugp/kenlm
# https://github.com/huggingface/huggingface_hub


def download_tmp():
    hf_hub_download(repo_id="edugp/kenlm", filename="wikipedia/en.arpa.bin")
    hf_hub_download(repo_id="edugp/kenlm", filename="wikipedia/en.sp.model")
    hf_hub_download(repo_id="edugp/kenlm", filename="model.py")

def download(repo_id: str, filename: str):
    hf_hub_download(repo_id=repo_id, filename=filename)

def download_repo(repo_id: str):
    snapshot_download(repo_id=repo_id)

def download_roberta():
    # when I want to use it, it will be downloaded
    from transformers import RobertaTokenizer, RobertaModel
    tokenizer = RobertaTokenizer.from_pretrained('roberta-large')
    model = RobertaModel.from_pretrained('roberta-large')

if __name__ == '__main__':
    # file_path = try_to_load_from_cache(repo_id="edugp/kenlm", filename="wikipedia/en.arpa.bin")
    # print(file_path)

    download_repo('roberta-large')