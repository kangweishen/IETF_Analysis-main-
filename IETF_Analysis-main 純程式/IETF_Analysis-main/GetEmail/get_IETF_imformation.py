import os
import pandas as pd
# Get Subject、From(sender)、Date、Link(mail)
from Subroutine.get_Infor import get_Information
# Get GW、Link(GW)、status
from Subroutine.get_IETF_WG_Link import get_IETF_WG_Link

# === 將 Subroutine 中擷取的資料存入 IETF_WG_Link.csv ===
# 儲存 輸出 & mail 資訊 csv 的資料夾名稱
folderpath = "get_information_csv"
if os.path.isdir(folderpath) == False:
    os.mkdir(folderpath)
    print("已建立資料夾 %s" % folderpath)

# === 透過 IETF_WG_Link.csv 中連結 擷取個工作組資料(主題、寄件人、日期、連結)分別存入 get_information_csv 資料夾 ===
if os.path.isfile("IETF_WG_Link.csv") == False:
    get_IETF_WG_Link()
IETF = pd.read_csv("IETF_WG_Link.csv", encoding="utf-8-sig")
wg_count = len(IETF)

folder = ["get_email_amount_csv", "get_subject_csv", "get_timeLine"]
png_path = [folder[0]+"/recipient_ChartBar/barChart_recipient_",
            folder[0]+"/recipient_ChartPie/pieChart_recipient_",
            folder[0]+"/sender_ChartBar/barChart_sender_",
            folder[0]+"/sender_ChartPie/pieChart_sender_",
            folder[1]+"/ChartBar/barChart_",
            folder[1]+"/ChartPie/pieChart_", folder[2]+"/timeLine_"]
for index in range(wg_count):

    wg_name = IETF["wg"][index]
    csv_name = "IETF_WG_Information_" + wg_name + ".csv"
    print("%4d/%4d: 正在擷取並儲存於 %s" % (index+1, wg_count, csv_name))
    csv_path = folderpath + "/" + csv_name
    if os.path.isfile(csv_path):
        df_csv = pd.read_csv(csv_path, encoding="utf-8-sig")
        previous_email_link = df_csv["Link"][0]
    else:
        previous_email_link = "create"

    link = IETF["link"][index]
    count = IETF["count"][index]
    page = int(count/40) + 2
    df = {"Subject": [], "From": [], "Date": [], "Link": []}
    df = pd.DataFrame(df)
    for num in range(1, page):
        new_df = get_Information(link+"&page="+str(num), previous_email_link)
        if new_df.index.stop == 0:
            break
        df = pd.concat([df, new_df], ignore_index=True)

    if df.empty == False:

        for path in png_path:
            if os.path.isfile(path + wg_name + ".png"):
                os.remove(path + wg_name + ".png")
        df = pd.concat([df, df_csv], ignore_index=True)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    else:
        continue
