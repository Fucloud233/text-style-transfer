from enum import Enum

# 评测维度
class EvalD(Enum):
    Style = 'style'
    Content = 'content'
    Fluency = 'fluency'