import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

# 儲存各別 WorkinkGroup 的 收、寄件人 資料
path = "get_email_amount_csv"
folderpath = [path, path+"/Category",
              path+"/sender_ChartBar", path+"/sender_ChartPie",
              path+"/recipient_ChartBar", path+"/recipient_ChartPie"]
for item in folderpath:
    if os.path.isdir(item) == False:
        os.mkdir(item)
        print("已建立資料夾", item)

# 讀取所有 WorkinkGroup 名稱
with open("IETF_WG_Link.csv", "rt", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    column_wg = [row_wg["wg"] for row_wg in reader]


def func(percent, part, total):
    quantity = int(round(percent / 100. * sum(part)))
    if len(total) > 10:
        return f"{quantity}封"
    else:
        return f"{percent:.1f}%"


wg_count = len(column_wg)  # 計數器(工作組)
for num in range(wg_count):

    csv_name = "get_information_csv/IETF_WG_Information_" + \
        column_wg[num] + ".csv"
    df = pd.read_csv(csv_name)

    # 計算 "寄件人" 信件數量
    sender = df["From"].value_counts().reset_index()
    sender.columns = ["From", "Count_From"]
    # 計算 "收件人" 信件數量
    receiver = df["Recipient"].value_counts().reset_index()
    receiver.columns = ["Recipient", "Count_Recipient"]

    # 將每個 WG 的結果保存到單獨的 DataFrame
    filepath = folderpath[1] + "/email_amount_" + column_wg[num] + ".csv"
    result = pd.concat([sender, receiver], axis=1)
    result.to_csv(filepath, index=False)
    print("%4d/%d：郵件數量 將儲存至 %s" % (num+1, wg_count, filepath))

    # ====== 寄件人 ======
    top_sender = sender.sort_values(["Count_From"], ascending=False).head(10)
    if len(top_sender) == 0:
        continue
    title = min(df["Date"].astype(str)) + " ~ " + \
        max(df["Date"].astype(str)) + "\n" + column_wg[num]
    if len(top_sender) == 10:
        title_sender = title + " 郵件數量前" + str(len(top_sender)) + " 多的寄件人"
    else:
        title_sender = title + " (" + str(len(top_sender)) + " 位寄件人)"

    # 繪製 "寄件人" 和 "寄件數量" 的長條圖
    SenderBarChartPath = folderpath[2] + \
        "/barChart_sender_" + column_wg[num] + ".png"
    if os.path.isfile(r"" + SenderBarChartPath) == False:
        try:
            amount = np.arange(len(top_sender)) + 1
            bar_sender = plt.barh(amount, top_sender["Count_From"])
            plt.bar_label(bar_sender, label_type="edge")
            plt.yticks(amount, top_sender["From"])
            plt.xlabel("郵件數量", fontsize=12)
            plt.ylabel("寄件人", fontsize=12)
            plt.title(title_sender, fontsize=14)
            plt.savefig(SenderBarChartPath, bbox_inches="tight")
        except:
            print(column_wg[num] + "無法繪製 寄件人 和 寄件數量 的長條圖")
        plt.close("all")

    # 繪製 "寄件人" 和 "寄件數量" 的圓餅圖
    SenderPieChartPath = folderpath[3] + \
        "/pieChart_sender_" + column_wg[num] + ".png"
    if os.path.isfile(r"" + SenderPieChartPath) == False:
        try:
            def autopct(x): return func(
                x, top_sender["Count_From"], sender["Count_From"])
            plt.pie(top_sender["Count_From"], labels=top_sender["From"],
                    autopct=autopct, startangle=90, radius=1.6,
                    textprops={'fontsize': 12})
            plt.title(title_sender, fontsize=14)
            plt.savefig(SenderPieChartPath, bbox_inches="tight")
        except:
            print(column_wg[num] + "無法繪製 寄件人 和 寄件數量 的圓餅圖")
        plt.close("all")

    # ====== 收件人 =======
    top_recipient = receiver.sort_values(
        ["Count_Recipient"], ascending=False).head(10)
    if len(top_recipient) == 0:
        continue
    elif len(top_recipient) == 10:
        title_recipient = title + " 郵件數量前" + str(len(top_recipient)) + " 多的收件人"
    else:
        title_recipient = title + " (" + str(len(top_recipient)) + " 位收件人)"

    # 繪製 "收件人" 和 "收件數量" 的長條圖
    RecipientBarChartPath = folderpath[4] + \
        "/barChart_recipient_" + column_wg[num] + ".png"
    if os.path.isfile(r"" + RecipientBarChartPath) == False:
        try:
            amount = np.arange(len(top_recipient)) + 1
            bar_recipient = plt.barh(amount, top_recipient["Count_Recipient"])
            plt.bar_label(bar_recipient, label_type="edge")
            plt.yticks(amount, top_recipient["Recipient"])
            plt.xlabel("郵件數量", fontsize=12)
            plt.ylabel("收件人", fontsize=12)
            plt.title(title_recipient, fontsize=14)
            plt.savefig(RecipientBarChartPath, bbox_inches="tight")
        except:
            print(column_wg[num] + "無法繪製 收件人 和 收件數量 的長條圖")
        plt.close("all")

    # 繪製 "收件人" 和 "收件數量" 的圓餅圖
    RecipientPieChartPath = folderpath[5] + \
        "/pieChart_recipient_" + column_wg[num] + ".png"
    if os.path.isfile(r"" + RecipientPieChartPath) == False:
        try:
            def autopct(x): return func(
                x, top_recipient["Count_Recipient"], receiver["Count_Recipient"])
            plt.pie(top_recipient["Count_Recipient"], labels=top_recipient["Recipient"],
                    autopct=autopct, startangle=90, radius=1.6,
                    textprops={'fontsize': 12})
            plt.title(title_recipient, fontsize=14)
            plt.savefig(RecipientPieChartPath, bbox_inches="tight")
        except:
            print(column_wg[num] + "無法繪製 收件人 和 收件數量 的圓餅圖")
        plt.close("all")

print("共 %d 個工作組儲存郵件主題分類結果\n" % wg_count)
