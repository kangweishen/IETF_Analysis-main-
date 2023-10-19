import re


def remove_short_and_long_words(text, min_length, max_length):
    # 定義正規表達式模式，以匹配單詞
    word_pattern = r'\b\w+\b'

    # 使用 findall 方法找到所有單詞
    words = re.findall(word_pattern, text)

    # 使用列表生成式過濾出符合條件的單詞
    filtered_words = [word for word in words if min_length <=
                      len(word) <= max_length]

    # 使用 join 方法將過濾後的單詞組合成新的文本
    filtered_text = ' '.join(filtered_words)

    return filtered_text


# 測試
input_text = "This is a test sentence with short and loooooong words"
min_length = 3
max_length = 6

filtered_text = remove_short_and_long_words(input_text, min_length, max_length)
print(filtered_text)
