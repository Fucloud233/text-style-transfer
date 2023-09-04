# GYAFC 数据集处理
使用GPT3.5对现有的GYAFC英文口语化/非口语的数据集进行翻译。

本部分的数据集主要包括两个部分：预处理和翻译。

## 预处理部分
> 文件路径: `preprocess.py`

预处理部分主要是将原有的数据集进行混合。
原有数据集两种不同的风格是分别存储在不同文件（`.src`/`.tgt`）中的。
这部分的意义在于将上述两种文件混合在同一个Json文件中，
方便后续翻译程序的编写。
> 注意: 在验证集中，`.tgt`文件中存在多个候选项，本程序默认选择第一个。

### 使用方法
输入参数:
* `base_file_path`: 数据集所在路径
* `dataset_type`: 数据集类型(test/train/valid)
* `ouput_name`: 输出名称
* `ouput_type`: 输出类型(json/txt)
* `ouput_path`: 输出路径
* `read_offset`: 读取起始值
* `read_size`: 读取大小（默认-1全部读取）

> 输出具体名称结合输出名称、输出路径和读取起始值大小决定的
> 
> 比如`{name}_{type}_{offset}_{offset+size}.{txt/json}`
> 
> 如果size=-1，则不会显示范围后缀

## 翻译部分
> 文件路径: `translate.py`

此部分是调用OpenAI的API，使用GPT3.5模型对该数据集进行翻译
### 使用方法
在使用之前需要在当前目录下的`config.json`文件中配置OpenAI密钥，格式如下
```json
{
  "api_key": "sk-XXX",
  "organization": "org-XXX"
}
```

输入参数
* `json_file_path`: 数据文件路径
* `offset`： 读取起始值
* `length`: 读取终止值
* `informal_output_file`: 口语化文本输出路径
* `formal_output_file`: 非口语化文本输出路径