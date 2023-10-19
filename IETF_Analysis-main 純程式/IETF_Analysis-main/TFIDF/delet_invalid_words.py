import re
import pandas as pd


# 去除無意義單詞
def delet_invalid_words(text):
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

    min_length = 4
    max_length = 10

    text = remove_short_and_long_words(text, min_length, max_length)

    url = "https://raw.githubusercontent.com/Alir3z4/stop-words/master/english.txt"
    stopWordsLink = pd.read_csv(url)
    for word in stopWordsLink.values:
        text = re.sub(r'[^\S](' + str(word[0]) + ')\s',
                      ' ', text.lower()).lower()
    text = re.sub(r'\d+[a-zA-Z]+', ' ', text.lower()).lower()
    text = re.sub(r'[\W][a-z]\s', ' ', text.lower()).lower()
    text = re.sub(r'[\n][a-z]\s', ' ', text.lower()).lower()
    text = re.sub(r'[\W][0-9]\s', ' ', text.lower()).lower()
    text = re.sub(r'[\n][0-9]\s', ' ', text.lower()).lower()
    text = re.sub(r'(\d+)[\s]', ' ', text.lower()).lower()
    text = re.sub(r'(gyan)', ' ', text.lower()).lower()
    return text.lower()


# 移除特殊字元，僅保留英數字及中日韓統一表意文字(CJK Unified Ideographs)
def CJK_cleaner(text):
    filters = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fff]+', re.UNICODE)
    return filters.sub(' ', text)  # 移除特殊字元


# 轉小寫並去除無意義內容(EX: 網址)
def delet_invalid_content(text):
    text = text.lower()
    text = re.sub(r'(\w+://[^\s]*)', ' ', text)
    text = re.sub(r'[^\S](thank).*', ' ', text)
    text = re.sub(r'(<.*>)', ' ', text)
    return text
