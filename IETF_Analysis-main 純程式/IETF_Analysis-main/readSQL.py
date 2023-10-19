# https://juejin.cn/s/python%20sqlite%20%E5%AF%BC%E5%87%BAcsv
import os
import csv
import sqlite3
import pandas as pd


def readsql(database, table, csv_name):

    conn = sqlite3.connect(database)  # 連接 SQLite 資料庫
    c = conn.cursor()
    c.execute("SELECT * FROM " + table)  # 查詢資料
    # 打開 CSV 文件並寫入資料
    with open(csv_name, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([i[0] for i in c.description])  # 寫入表頭
        writer.writerows(c)  # 寫入資料
    conn.close()  # 關閉連接


database = ["sqlite3/IETF_WG_Link.db", "sqlite3/mailingLists.db",
            "sqlite3/get_email_amount_csv.db", "sqlite3/get_information_csv.db",
            "sqlite3/get_subject_csv.db", "sqlite3/IETF工作組_基本資訊.db"]
folderpath = ["get_email_amount_csv/Category", "get_information_csv",
              "get_subject_csv/Category", "IETF工作組_基本資訊/IETF_Basic_Info"]
csv_name = ["IETF_WG_Link", "mailingLists", folderpath[0]+"/email_amount_",
            folderpath[1]+"/IETF_WG_Information_",
            folderpath[2]+"/subject_Classification_", folderpath[3]+"/"]

for path in folderpath:
    if not os.path.isdir(path):
        os.makedirs(path)

for i in range(2):
    readsql(database[i], csv_name[i], csv_name[i]+".csv")

IETF = pd.read_csv("IETF_WG_Link.csv", encoding="utf-8")
wg_count = len(IETF)

for i in range(2, 5):
    for index in range(wg_count):
        wg_name = IETF["wg"][index]
        try:
            readsql(database[i], wg_name, csv_name[i]+wg_name+".csv")
        except:
            # OperationalError: unrecognized token
            readsql(database[i], "'"+wg_name+"'", csv_name[i]+wg_name+".csv")

basic_name = ["IETF_WG_Active", "datatracker", "IETF_WG_Link", "mailarchive"]
for name in basic_name:
    readsql(database[5], name, csv_name[5]+name+".csv")
