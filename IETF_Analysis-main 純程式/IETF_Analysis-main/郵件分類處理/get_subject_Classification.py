import re
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 字體設定
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False  # 正常顯示負號

# 創建儲存 WorinkingGroup 分類結果的資料夾(get_subject_csv)
path = "get_subject_csv"
folderpath = [path, path+"/Category", path+"/ChartBar", path+"/ChartPie"]
for item in folderpath:
    if os.path.isdir(item) == False:
        os.mkdir(item)
        print("已建立資料夾", item)

# 讀取所有 WorinkingGroup 名稱
with open("IETF_WG_Link.csv", "rt", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    column_wg = [row_wg["wg"] for row_wg in reader]

# 判斷 classify 裡是否存在至少一個 string


def exist(string):
    return classify["Subject"].isin([string]).any()

# 數量加1、更改最新日期、增加種類名稱


def modify(string):
    classify.at[position[string], "Count"] += 1
    classify.at[position[string], "Updated"] = date
    category.append(string)

# 圓餅圖的標籤內容


def func(percent, part, total):
    quantity = int(round(percent / 100. * sum(part)))
    if len(total) > 10:
        return f"{quantity}封"
    else:
        return f"{percent:.1f}%\n{quantity}封"


wg_count = len(column_wg)
for index in range(wg_count):

    csv_path = "get_information_csv/IETF_WG_Information_" + \
        column_wg[index] + ".csv"
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print("%4d/%d: 郵件類別 正在分類至 %s" % (index+1, wg_count, csv_path))

    email_subject = []
    amount = len(df["Subject"])
    if "Category" in df.columns:
        for link_index in range(amount):
            if pd.isnull(df["Category"][link_index]):
                email_subject.append(df["Subject"][link_index])
            else:
                break
    else:
        email_subject = df["Subject"]
    subject_amount = len(email_subject)
    if subject_amount == 0:
        continue

    CategoryPath = folderpath[1] + "/subject_Classification_" + \
        column_wg[index] + ".csv"
    if os.path.isfile(r"" + CategoryPath):
        classify = pd.read_csv(CategoryPath, encoding="utf-8-sig")
    else:
        classifcation = {"Subject": [], "Count": [], "Updated": []}
        classify = pd.DataFrame(classifcation)

    category = []
    position = {}
    category_index = 0
    for subject_index in range(subject_amount-1, -1, -1):
        try:
            date = df["Date"][subject_index]
            subject = email_subject[subject_index]
            a = re.sub(r"Re\:\s", "", subject)
            b = re.sub(r"\[.*\]\s", "", a)
            c = re.sub(r"Reminder:\s", "", b)
            if exist(subject) == exist(a) == exist(b) == exist(c) == False:
                new_row = pd.DataFrame(
                    {"Subject": [c], "Count": [1], "Updated": date})
                classify = pd.concat([classify, new_row], ignore_index=True)
                position[c] = category_index
                category_index += 1
                category.append(c)
            elif exist(subject):
                modify(subject)
            elif exist(a):
                modify(a)
            elif exist(b):
                modify(b)
            elif exist(c):
                modify(c)
        except:
            category.append("")
            continue

    # 將種類結果放至 資料夾(get_subject_csv)所屬的工作組檔案中做儲存
    classify["Count"] = pd.to_numeric(classify["Count"], downcast="integer")
    classify["Updated"] = pd.to_datetime(classify["Updated"])
    classify.to_csv(CategoryPath, encoding="utf-8-sig", index=False)
    # 將種類結果放至 資料夾(get_information_csv)所屬的工作組檔案中做儲存
    if "Category" in df.columns:
        for num in range(subject_amount):
            df.at[num, "Category"] = category[subject_amount-num-1]
    else:
        df.insert(6, "Category", category[::-1], True)
    df.to_csv(csv_path, encoding="utf-8-sig", index=False)

    top = classify.sort_values(["Count", "Updated"], ascending=False).head(10)
    if len(top) == 0:
        continue
    df["Date"] = df["Date"].astype(str)
    title = min(df["Date"]) + " ~ " + max(df["Date"]) + "\n" + column_wg[index]
    if len(top) == 10:
        title += " 郵件數量前 " + str(len(top)) + " 多的郵件主題"
    else:
        title += " (" + str(len(top)) + "種郵件主題)"

    # 長條圖
    BarChartPath = folderpath[2] + "/barChart_" + column_wg[index] + ".png"
    if os.path.isfile(r"" + BarChartPath) == False:
        try:
            amount = np.arange(len(top)) + 1
            p1 = plt.barh(amount, top["Count"])
            plt.bar_label(p1, label_type="edge")
            plt.yticks(amount, top["Subject"])
            plt.xlabel("郵件數量", fontsize=14)
            plt.ylabel("郵件種類", fontsize=14)
            plt.title(title, fontsize=16)
            plt.savefig(BarChartPath, bbox_inches="tight")
        except:
            print(column_wg[index] + "無法繪製 長條圖")
        plt.close("all")

    # 圓餅圖
    PieChartPath = folderpath[3] + "/pieChart_" + column_wg[index] + ".png"
    if os.path.isfile(r"" + PieChartPath) == False:
        try:
            def autopct(x): return func(x, top["Count"], classify["Count"])
            plt.pie(top["Count"], labels=top["Subject"], autopct=autopct,
                    startangle=90, radius=1.5, textprops={'fontsize': 14})
            plt.title(title, fontsize=16)
            plt.savefig(PieChartPath, bbox_inches="tight")
        except:
            print(column_wg[index] + "無法繪製 圓餅圖")
        plt.close("all")
