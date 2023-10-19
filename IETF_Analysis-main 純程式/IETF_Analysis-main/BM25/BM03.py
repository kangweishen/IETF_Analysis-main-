def BM(WG, query):
    ''' BM03.py '''
    from rank_bm25 import BM25Okapi
    import pandas as pd
    import csv

    # === NLP summarize lib ===
    from BM25.mkSummText import mkSummText

    # === wordcloud ===
    from BM25.mkCloud import mkCloud

    ''' main flow '''
    # load from csv
    df = pd.read_csv('get_information_csv/IETF_WG_Information_' +
                     WG + '.csv', encoding="utf-8-sig")

    mail = df[['Subject', 'Content']]

    mailtitle = mail['Subject'].astype(str)
    mailimdb = mail['Content'].astype(str)

    # --- tokenize
    tokenized_corpus = [doc.split(" ") for doc in mailimdb]

    # --- initiate
    bm = BM25Okapi(tokenized_corpus)

    tokenized_query = query.split(" ")

    # 計算 BM25 score (log)
    scores = bm.get_scores(tokenized_query)
    idx = scores.argmax()

    if idx != 0:
        # 開啟輸出的 CSV 檔案
        imdbTxt = mailimdb[idx]
        with open('BM25/BM25_output.csv', 'w', newline='', encoding="utf-8") as csvfile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvfile)

            # 寫入一列資料
            writer.writerow(['Match No.', 'score', 'Mail Subject',
                            'Mail Content', 'Each mail score', 'Total number of mail'])

            # 寫入另外幾列資料
            writer.writerow([f'idx: {idx}', scores[idx], mailtitle[idx],
                             imdbTxt[:-1], scores, len(scores)])
        mkCloud(imdbTxt)
        sumTxt = mkSummText(imdbTxt)

    with open('BM25/BM25_summary.csv', 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Mail summary'])
        for s in sumTxt:
            writer.writerow([s])
