from huggingface_hub import hf_hub_download

# https://huggingface.co/edugp/kenlm
# https://github.com/huggingface/huggingface_hub

# hf_hub_download(repo_id="edugp/kenlm", filename="wikipedia/en.arpa.bin")
hf_hub_download(repo_id="edugp/kenlm", filename="model.py")
