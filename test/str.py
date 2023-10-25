
def test_LP():
    # 在format中输出{}，比如重复一遍
    format_str = "Here is some text: {}. Here is a rewrite of the text, which is more positive: {{"

    input = "hello"
    output = format_str.format(input)

    print(output)

if __name__ == '__main__':
    test_LP()