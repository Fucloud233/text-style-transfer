# Text-Style-Transfer 实验

## Config

如果你涉及到需要调用Openai的api，请在项目根目录下创建文件`config.json`，并填入以下内容。
```json
{
    "openai-key": "sk-xxx"
}
```

在配置好api的key后，请安装一下依赖。
```
tqdm # 进度显示
fire # 快速创建cli
openai # openai sdk
```

## Evaluate

请按照以下顺序配置相关文件进行评测。

### 评测配置文件

当你需要评测时，请先编写好评测配置文件，

* `k`: 需要评测的前k条数据
* `style_type`/`style1`: 由于prompt设计，你需要制定风格的类型，和迁移后的风格类型
    
    > 详情请见[评测Prompts](data/eval_prompts.json)
* `sentences_path`: 评测句子的文件（文件格式见后方）
* `prompt_template_path`: 评测prompt的路径
* `output_path`: 输出路径


```json
{
    "k": 2,
    "style_type": "sentiment",
    "style1": "positivity",
    "sentences_path": ,
    "prompt_template_path": "data/eval_prompts.json",
    "output_path": 
}
```

### 句子文件格式
输入数据格式如以下所示，0表示原句子，1表示迁移后的句子。
```json
[
    {
        "0": "source",
        "1": "target"
    }
]

```

### 运行程序

请在根目录下运行以下指令即可开始评测，`eval_config.json`为评测配置文件。
```bash
python3 src/evaluation.py eval_config.json
```
