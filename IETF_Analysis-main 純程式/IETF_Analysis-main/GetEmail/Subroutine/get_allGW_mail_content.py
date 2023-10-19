import csv
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

csv.field_size_limit(500 * 1024 * 1024)

# 抓取各個 Working Group 名稱
with open("IETF_WG_Link.csv", "rt", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    column_wg = [row_wg["wg"] for row_wg in reader]

# ====== 截取郵件內容 ======
# 計算 Working Group 數量
WGlinkcount = len(column_wg)
run = 100/WGlinkcount

# 用名稱 -> 郵件連結 -> 截取郵件內容
with tqdm(total=100) as pbar:

    for WGFileName in range(WGlinkcount):
        pbar.update(run)
        tar_WGFileName = "get_information_csv\IETF_WG_Information_" + \
            column_wg[WGFileName] + ".csv"
        # 存放各 working group mail 的檔案名稱
        df_csv = pd.read_csv(tar_WGFileName, encoding="utf-8-sig")
        # 讀取儲存之前擷取的資料

        email_link = []
        link_count = len(df_csv["Link"])
        if "Content" in df_csv.columns:
            for link_index in range(link_count):
                if pd.isnull(df_csv["Content"][link_index]):
                    email_link.append(df_csv["Link"][link_index])
        else:
            email_link = df_csv["Link"]

        count = len(email_link)
        if count == 0:
            continue
        print("\n正在擷取 " + column_wg[WGFileName] + " 郵件內容")

        mailTxT = []  # 用來儲存郵件內容
        for link_mail in email_link:
            try:
                r = requests.get(link_mail)
                # 藉由 郵件網址 將此頁面的 HTML GET 下來
                soup = BeautifulSoup(r.text, "html.parser")
                # 先變成 text 形式，再以 Beautiful Soup 解析 HTML 程式碼
                mail_text = soup.find(class_="msg-payload").get_text()
                # 找出 郵件內容 的網頁元素資料的 text
                mailTxT.append(mail_text)
            except:
                mailTxT.append("")
                continue

        if "Content" in df_csv.columns:
            for num in range(len(mailTxT)):
                df_csv.at[num, "Content"] = mailTxT[num]
        else:
            df_csv.insert(4, "Content", mailTxT, True)  # 將郵件內容插入至最後列儲存
        df_csv.to_csv(tar_WGFileName, encoding="utf-8-sig", index=False)
