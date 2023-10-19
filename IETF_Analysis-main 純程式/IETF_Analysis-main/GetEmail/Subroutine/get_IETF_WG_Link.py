# 目的：正規表達式找出 HTML 中的 href (網址)
import re
# 目的：用來與網頁取得資源
import requests
import pandas as pd
# 目的：用來處理 HTML 文本內的特定標籤或類別等
from bs4 import BeautifulSoup
# Get messages number
from Subroutine.get_MC import get_message_count


def get_IETF_WG_Link():

    url = "https://mailarchive.ietf.org/arch/browse/"
    r = requests.get(url)
    # 轉成 text 形式，並以 Beautiful Soup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, "html.parser")
    # (in)active-lists
    active = soup.findAll(id="active-lists")
    inactive = soup.findAll(id="inactive-lists")

    # 找出 (in)active 相關的 wg 連結 name
    active_name = re.findall(r'"/arch/browse/(\S*)/"', str(active))
    inactive_name = re.findall(r'"/arch/browse/(\S*)/"', str(inactive))
    # 刪除 static
    active_name.remove(active_name[0])
    wg = active_name + inactive_name
    print("  Active Lists:", len(active_name))
    print("Inactive Lists:", len(inactive_name))

    link = []  # 放工作組郵件信箱連結
    status = []  # 活躍/不活躍

    # 合成成郵件信箱連結
    for name in active_name:
        status.append("active")
        link.append(url + name + "/?qdr=y")
    for name in inactive_name:
        status.append("inactive")
        link.append(url + name + "/?qdr=y")

    # 將0封以外的郵件相關資訊存檔
    amount = len(wg)
    count = {}
    wg_new = []
    link_new = []
    status_new = []
    count_new = []
    for index in range(amount):
        count[index] = get_message_count(link[index])
        if count[index] == 0:
            print("%4d/%4d: %6s messages (%s)" %
                  (index+1, amount, count[index], wg[index]))
        else:
            wg_new.append(wg[index])
            link_new.append(link[index])
            status_new.append(status[index])
            count_new.append(count[index])
            print("%4d/%4d: %6s messages (%s)" %
                  (index+1, amount, count[index], wg[index]))

    df = pd.DataFrame({"wg": wg_new, "link": link_new,
                      "status": status_new, "count": count_new})
    df.to_csv("IETF_WG_Link.csv", encoding="utf-8-sig", index=False)
    print("IETF_WG_Link.csv 完成存檔\n")
