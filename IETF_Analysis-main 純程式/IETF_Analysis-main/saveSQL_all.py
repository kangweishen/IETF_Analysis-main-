import os
import sqlite3
import pandas as pd
db_path = "IETF.db"
if os.path.isfile(db_path):
    os.remove(db_path)

name = ["IETF_WG_Link", "get_information_csv", "get_email_amount_csv",
        "get_subject_csv", "IETF工作組_基本資訊", "mailingLists"]


def data_table_processing(csv_path, wg_name):
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    column = df.columns
    df["wg"] = wg_name
    df = df.reindex(columns=["wg"]+list(column))
    return df


# IETF_WG_Link.csv 轉換成 IETF_WG_Link.db
# 讀取CSV資料集檔案
IETF = pd.read_csv(name[0] + ".csv", encoding="utf-8")
wg_count = len(IETF)
column0 = IETF.columns
conn = sqlite3.connect(db_path)  # 同時建立資料庫與連線
cursor = conn.cursor()  # 建立資料庫操作指標
cursor.execute("CREATE TABLE " + name[0] + "(" +
               column0[0] + " TEXT PRIMARY KEY NOT NULL," +
               column0[1] + " TEXT NOT NULL," + column0[2] + " TEXT NOT NULL," +
               column0[3] + " INTEGER NOT NULL)")  # 執行新增資料表的SQL指令
cursor.close()
conn.commit()  # 確認完成
# 如果資料表存在，就寫入資料，否則建立資料表
IETF.to_sql(name[0], conn, if_exists="append", index=False)
conn.close()

# get_information_csv 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(db_path)
for index in range(wg_count):
    wg_name = IETF["wg"][index]
    table_name = "IETF_WG_Information_" + wg_name
    csv_path = name[1] + "/" + table_name + ".csv"
    df = data_table_processing(csv_path, wg_name)
    conn.commit()
    df.to_sql(table_name, conn, if_exists="append", index=False)
conn.close()

# get_email_amount_csv 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(db_path)
for index in range(wg_count):
    wg_name = IETF["wg"][index]
    table_name = "email_amount_" + wg_name
    csv_path = name[2] + "/Category/" + table_name + ".csv"
    df = data_table_processing(csv_path, wg_name)
    conn.commit()
    df.to_sql(table_name, conn, if_exists="append", index=False)
conn.close()

# get_subject_csv 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(db_path)
for index in range(wg_count):
    wg_name = IETF["wg"][index]
    table_name = "subject_Classification_" + wg_name
    csv_path = name[3] + "/Category/" + table_name + ".csv"
    df = data_table_processing(csv_path, wg_name)
    conn.commit()
    df.to_sql(table_name, conn, if_exists="append", index=False)
conn.close()

# IETF_Basic_Info 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(db_path)
csv_name = ["IETF_WG_Active", "datatracker", "IETF_WG_Link", "mailarchive"]
for index in range(len(csv_name)):
    table_name = "IETF_Basic_Info/" + csv_name[index]
    df = pd.read_csv(name[4] + "/" + table_name + ".csv", encoding="utf-8-sig")
    conn.commit()
    df.to_sql(table_name, conn, if_exists="append", index=False)
conn.close()

# mailingLists.csv 轉換成 mailingLists.db
df = pd.read_csv(name[5] + ".csv", encoding="utf-8")
column5 = df.columns
conn = sqlite3.connect("IETF.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE " + name[5] + "(" +
               column5[0] + " TEXT PRIMARY KEY NOT NULL," +
               column5[1] + " TEXT NOT NULL," + column5[2] + " TEXT NOT NULL)")
cursor.close()
conn.commit()
df.to_sql(name[5], conn, if_exists="append", index=False)
conn.close()
