# === 提供主題做選擇 ===
def Select_Subject(WG):

    # 選擇類別 & 提供選項
    import pandas as pd

    df_subject = pd.read_csv("get_subject_csv/Category/subject_Classification_" + WG + ".csv",
                             usecols=["Subject"])  # 可調整

    list_subject = df_subject["Subject"].tolist()

    return list_subject


# === 以TF-IDF演算法 統計計算出關鍵字 ===
def TFIDF(WG, ChooseSubject):

    import pandas as pd
    import jieba
    import math
    from wordcloud import WordCloud

    # 抓 "指定主題" & "所有內容"
    df_AllContent = pd.read_csv("get_information_csv/IETF_WG_Information_" + WG + ".csv",
                                usecols=["Content", "Category"])  # 可調整

    # 篩選出選擇主題內容
    df_ChooseContent = df_AllContent[df_AllContent["Category"]
                                     == ChooseSubject]

    # 篩選出選擇主題外的內容
    df_otherContent = df_AllContent[df_AllContent["Category"] != ChooseSubject]
    list_ChooseContent = df_ChooseContent["Content"].tolist()
    list_otherContent = df_otherContent["Content"].tolist()

    # 載入郵件內容
    text_a = ' '.join(list_ChooseContent)
    text_b = ' '.join(list_otherContent)

    # 移除介係詞等預處理
    from TFIDF.delet_invalid_words import delet_invalid_words, CJK_cleaner, delet_invalid_content

    # 轉小寫並去除無意義內容(EX: 網址)
    text_a = delet_invalid_content(text_a)
    text_b = delet_invalid_content(text_b)

    # 去除特殊字元
    text_a = CJK_cleaner(text_a)
    text_b = CJK_cleaner(text_b)

    # 去除無意義單詞
    text_a = delet_invalid_words(text_a)
    text_b = delet_invalid_words(text_b)

    # 分詞
    from nltk.tokenize import word_tokenize
    slide_text_a = word_tokenize(text_a)
    slide_text_b = word_tokenize(text_b)

    # 轉小寫後 去除介係詞等...停用詞
    def content_fraction(text):
        import nltk.corpus
        nltk.download("stopwords")
        from nltk.corpus import stopwords
        stopwords = nltk.corpus.stopwords.words("english")
        content = [w for w in text if w.lower() not in stopwords]
        return content

    # 將預處理完的郵件拼回去
    text_a = ' '.join(content_fraction(slide_text_a))
    text_b = ' '.join(content_fraction(slide_text_b))

    # jieba分詞處理 並建立詞庫
    texta_seg = jieba.lcut(text_a)
    textb_seg = jieba.lcut(text_b)
    unique_words = set(texta_seg).union(set(textb_seg))  # 所有文件中的單詞(文字庫)

    # 建立2個新字典，分別存2篇文章詞的出現次數
    num_words_a = dict.fromkeys(unique_words, 0)
    num_words_b = dict.fromkeys(unique_words, 0)

    for word in texta_seg:
        num_words_a[word] += 1

    for word in textb_seg:
        num_words_b[word] += 1

    def get_TF_value(w_dict, text_seg_len):
        tf_dict = {}

        for w, count in w_dict.items():
            # 計算tf的公式
            tf_dict[w] = count / float(text_seg_len)

        return tf_dict

    def get_IDF_value(text_list, all_words):

        idf_dict = dict.fromkeys(all_words.keys(), 0)

        for text in text_list:
            for w, val in text.items():
                # 表示出現過在一次文本中
                if val > 0:
                    idf_dict[w] += 1

        for w, val in idf_dict.items():
            # 計算idf的公式
            idf_dict[w] = math.log(len(text_list) / float(val))
        return idf_dict

    tf_a = get_TF_value(num_words_a, len(texta_seg))
    tf_b = get_TF_value(num_words_b, len(textb_seg))

    idf = get_IDF_value([num_words_a, num_words_b], num_words_a)

    # 計算tfidf
    tfidf_a = {}
    tfidf_b = {}
    for w, val in tf_a.items():
        tfidf_a[w] = val * idf[w]

    for w, val in tf_b.items():
        tfidf_b[w] = val * idf[w]

    WordCloud(collocations=False, width=600,  # 圖片寬度
              height=600,  # 圖片高度
              background_color="white",  # 圖片底色
              margin=2  # 文字之間的間距
              ).generate_from_frequencies(tfidf_a).to_image().save("tfidf_wordcloud.png")
