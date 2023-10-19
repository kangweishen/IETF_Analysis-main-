import os
import shutil
import sqlite3
import pandas as pd

name = ["IETF_WG_Link", "get_information_csv", "get_email_amount_csv",
        "get_subject_csv", "IETF工作組_基本資訊", "mailingLists"]
path = "sqlite3"
if os.path.isdir(path):
    shutil.rmtree(path)
os.mkdir(path)
print("已建立資料夾", path)

print("儲存資料入資料庫請稍後")
# IETF_WG_Link.csv 轉換成 IETF_WG_Link.db
IETF = pd.read_csv(name[0] + ".csv")
wg_count = len(IETF)
column0 = IETF.columns
conn = sqlite3.connect(path + "/" + name[0] + ".db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE " + name[0] + "(" +
               column0[0] + " TEXT PRIMARY KEY NOT NULL," +
               column0[1] + " TEXT NOT NULL," + column0[2] + " TEXT NOT NULL," +
               column0[3] + " INTEGER NOT NULL)")
cursor.close()
conn.commit()
IETF.to_sql(name[0], conn, if_exists="append", index=False)
conn.close()

# get_information_csv 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(path + "/" + name[1] + ".db")
for index in range(wg_count):
    wg_name = IETF["wg"][index]
    df = pd.read_csv(name[1] + "/IETF_WG_Information_" + wg_name + ".csv")
    conn.commit()
    df.to_sql(wg_name, conn, if_exists="append", index=False)
conn.close()

# get_email_amount_csv 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(path + "/" + name[2] + ".db")
for index in range(wg_count):
    wg_name = IETF["wg"][index]
    df = pd.read_csv(name[2] + "/Category/email_amount_" + wg_name + ".csv")
    conn.commit()
    df.to_sql(wg_name, conn, if_exists="append", index=False)
conn.close()

# get_subject_csv 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(path + "/" + name[3] + ".db")
for index in range(wg_count):
    wg_name = IETF["wg"][index]
    df = pd.read_csv(
        name[3] + "/Category/subject_Classification_" + wg_name + ".csv")
    conn.commit()
    df.to_sql(wg_name, conn, if_exists="append", index=False)
conn.close()

# IETF_Basic_Info 資料夾裡的 .csv 轉換成 .db
conn = sqlite3.connect(path + "/" + name[4] + ".db")
csv_name = ["IETF_WG_Active", "datatracker", "IETF_WG_Link", "mailarchive"]
for index in range(len(csv_name)):
    df = pd.read_csv(name[4] + "/IETF_Basic_Info/" + csv_name[index] + ".csv")
    conn.commit()
    df.to_sql(csv_name[index], conn, if_exists="append", index=False)
conn.close()

# mailingLists.csv 轉換成 mailingLists.db
df = pd.read_csv(name[5] + ".csv")
column5 = df.columns
conn = sqlite3.connect(path + "/" + name[5] + ".db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE " + name[5] + "(" +
               column5[0] + " TEXT PRIMARY KEY NOT NULL," +
               column5[1] + " TEXT NOT NULL," + column5[2] + " TEXT NOT NULL)")
cursor.close()
conn.commit()
df.to_sql(name[5], conn, if_exists="append", index=False)
conn.close()
