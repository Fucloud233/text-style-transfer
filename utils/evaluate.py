# import math
import numpy as np
from enum import Enum
from typing import List

# 评测维度
class EvalMetric(Enum):
    Style = 'style'
    Content = 'content'
    Fluency = 'fluency'
    GM = "GM"
    HM = "HM"

    def __str__(self):
        return self.value

def geometric_mean(data: List[float]) -> float:
    return np.sqrt(np.prod(data))

def harmonic_mean(data: List[float]) -> float:
    return 1 / np.average(np.divide(1, data))

def test_mean():
    data = [39.4, 33.1]
    print(geometric_mean(data), harmonic_mean(data))
    pass

if __name__ == '__main__':
    # test_mean()

    # print (f"%.{2}f" % 1.333)
    print(EvalMetric.Style)
