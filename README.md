# 文本风格迁移

## 数据集处理
1. 将GYAFC数据集翻译成中文
2. 央视新闻爬虫
3. ...

## 1. GYAFC 数据集处理程序
* 数据来源: https://aclanthology.org/N18-1012/
* 下载地址: https://huggingface.co/datasets/RUCAIBox/Style-Transfer
* 所在位置: `GYAFC Dataset/code`

### 数据集介绍
这个数据包括两个领域的数据
* em: Entertainment & Music 
* fr: Family & Relationships

其中每个领域包括三类数据集 (train, test, valid), 
其中informal在`.src`，formal中`.tgt`中,
train中两种风格文本一一配对，test和valid中则是一对多配对

### 使用方法 
1. 打开`code/main.py`
2. 然后配置主函数中的各个参数
3. 再在`GYAFC Dataset`路径下运行该程序
   在其他路径下运行可能会影响输入和输出的位置

## 2. 央视新闻爬虫
* 引用代码: https://github.com/CreateSun/NewsSpiderBasedOnScrapy

### 工作步骤
1. 使用`scrapy`库爬取央视新闻某个分区的新闻
2. 按照段落进行划分
3. 然后根据字数对划分的内容进行筛选