import os
import pandas as pd
import matplotlib.pyplot as plt

# 創建 "儲存時間軸圖片" 的資料夾
folderpath = "get_timeLine"
if not os.path.isdir(folderpath):
    os.mkdir(folderpath)
    print("已建立資料夾", folderpath)

# 讀取所有 WorkingGroup 資料
IETF = pd.read_csv("IETF_WG_Link.csv", encoding="utf-8-sig")
# 計算 WorkingGroup 數量
wg_count = len(IETF)

for num in range(wg_count):
    # 存放各 WG 資訊的檔案名稱
    Timeline = "get_timeLine/timeLine_" + IETF["wg"][num] + ".png"
    if os.path.isfile(r"" + Timeline):
        continue
    csv_name = "get_information_csv/IETF_WG_Information_" + \
        IETF["wg"][num] + ".csv"
    df = pd.read_csv(csv_name, encoding="utf-8-sig")

    # 將 日期資料 轉換為 年月資料
    newdate = df["Date"].astype(str)
    newdatecount = len(newdate)
    for index in range(newdatecount):
        newdate[index] = newdate[index][0:7]
    # 計算每個年月的數量
    amount = newdate.value_counts()
    # 按照日期排序
    amount = amount.sort_index()

    # 創建折線圖
    plt.xticks(rotation=45)
    plt.plot(amount.index, amount.values)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.title("Time Series Plot: " + IETF["wg"][num], fontsize=14)
    for x, y in zip(amount.index, amount.values):
        plt.text(x, y, y, fontsize=14)
    plt.savefig(Timeline, bbox_inches="tight")
    plt.close('all')
    print("%4d/%d: 時間軸 已儲存至 %s" % (num+1, wg_count, Timeline))
