from huggingface_hub import hf_hub_download, try_to_load_from_cache

# https://huggingface.co/edugp/kenlm
# https://github.com/huggingface/huggingface_hub


def download():
    hf_hub_download(repo_id="edugp/kenlm", filename="wikipedia/en.arpa.bin")
    hf_hub_download(repo_id="edugp/kenlm", filename="wikipedia/en.sp.model")
    hf_hub_download(repo_id="edugp/kenlm", filename="model.py")


if __name__ == '__main__':
    # file_path = try_to_load_from_cache(repo_id="edugp/kenlm", filename="wikipedia/en.arpa.bin")
    # print(file_path)

    download()