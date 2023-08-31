# -*- coding = utf-8 -*-
# @Time : 2023/08/30 22:13
# @Autor : Fucloud
# @FIle : config.py.py
# @Software : PyCharm

import json


def config() -> dict:
    file_path = "config.json"
    with open(file_path, "r") as f:
        config_text = '\n'.join(f.readlines(-1))

    config_json = json.loads(config_text)

    return config_json

