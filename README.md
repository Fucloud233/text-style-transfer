# Text-Style-Transfer 实验

## Config

如果你涉及到需要嗲用Openai的api，请在项目根目录下创建文件`config.json`，并填入以下内容。
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

### 输入数据

#### 句子
输入数据格式如以下所示。
```json
[
    {
        "0": "source",
        "1": "target"
    }
]

```

#### Prompt Templates
Prompt模板存储在`data/eval_prompts.json`中，程序会自动读取。

#### 使用

请在根目录下运行以下指令。
```bash
python3 src/evaluation.py -k=_ -sentenes_path=_
```
