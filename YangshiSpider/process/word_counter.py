from matplotlib import pyplot as plt

""" Refer
* https://blog.csdn.net/qq_29721419/article/details/71638912
"""


class WordCounter:
    def __init__(self):
        self.record_counter: dict = {}

    def add_text(self, text: str):
        text_length = len(text)
        if text_length not in self.record_counter:
            self.record_counter[text_length] = 1
        else:
            self.record_counter[text_length] += 1

    def display(self):
        for (key, value) in self.record_counter.items():
            print("Length = {}: {}".format(key, value))

    # 使用matplotlib进行绘图
    def display_graph(self):
        x = self.record_counter.keys()
        y = self.record_counter.values()

        # 计算最大值
        # max_y = max(y)
        # for _x in x:
        #     if self.record_counter[_x] == max_y:
        #         print("[debug] x[{}] = {}: ".format(_x, max_y))
        #         break

        plt.bar(x, y)

        plt.show()


if __name__ == "__main__":
    test_texts = {
        "Hello", "world", "a", "abc"
    }

    counter = WordCounter()
    for t in test_texts:
        counter.add_text(t)

    counter.display()
    counter.display_graph()
