# -*- coding = utf-8 -*-
# @Time : 2023/07/26 16:34
# @Autor : Fucloud
# @FIle : test_path.py
# @Software : PyCharm

from pathlib import Path

if __name__ == "__main__":
    # file_name = "test.py"
    file_name = "test"
    file_path = Path(file_name)

    print("[debug] Suffix: ", file_path.suffix)
    file_path = file_path.with_suffix(".doc")

    print("[debug] Suffix: %s, Name: %s " % (file_path.suffix, file_path.name))
