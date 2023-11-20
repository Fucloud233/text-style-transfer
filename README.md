# Text-Style-Transfer 实验

## Config

本代码中在评测过程中使用了openai的API，
所以如果你需要评测结果，
请在项目根目录下创建文件`config.json`，并填入以下内容。
```json
{
    "openai-key": "sk-xxx"
}
```

在配置好api的key后，请安装`requirement.txt`中所需要的依赖。

## Transfer

风格迁移需要通过配置文件进行配置

```json
{
    // test dataset loading
    "k": 100,
    "load_type": "random",
    "dataset_path": "",
    "output_path": "",

    // transfer prompt
    "prompt": "",
    
    // (option) use retrieval
    "retrieval_path": "",
    "retrieval_type": "bm25"
}
```

运行方式
```bash
python src/transfer.py TRANSFER_CONFIG_PATH
```

## Evaluate

### 迁移结果的文件格式

输入数据格式如以下所示，0表示原句子，1表示迁移后的句子。

```json
[
    {
        "0": "source",
        "1": "target"
    }
]

```

### 安装依赖

* tqdm: 显示运行进度
* transformers (hugging face): 用于运行Roberta模型
* evaluate (hugging face): 用于运行sacre_bleu
* kenlm, sentencepiece, huggingface_hub: 用于运行Kenlm

由于本评估其使用`Roberta`对风格迁移准确率进行评估，
因此请下载好经过预训练的模型，并放在`model/roberta`目录下。

### 编辑运行配置

请打开`src/evaluate/main.py`，并找到`main`函数。
主要的运行代码如下所示

```python
# 1. 初始化评测器
evaluator = Evaluator()
# 2. 添加需要评测的句子
evaluator.append_results(
    names, 
    results_path, 
    filename=TRANSFER_OUTPUT_FILE
)
# 3. 开始评测
evaluator.evaluate(
    output_path,
    filename=EVALUATE_OUTPUT_FILE
)
```

#### 2. 添加需要评测的结果

该函数一下三个参数，
这样设计是为了方便批量评测不同方法下的迁移结果。

* `names`: 使用方法的名字
* `results_path`：迁移结果所在路径
* `filename`: 迁移结果的文化名

换句话说，
程序会自动查找`results_path/name/filename`文件作为迁移结果。
其中`filename`默认为`transfer.json`，其格式如上所示。

#### 3. 开始评测

该函数有两个参数，主要是设定输出路径和输出文件名。
换句话说，评测结果会保存在`output_path/filename`的文件中。
其中`filename`默认为`evaluate.json`。

### 运行程序

请保证工作路径在项目的根目录中，然后在命令行中输入以下代码。
```sh
python src/evaluate/main.py
```
