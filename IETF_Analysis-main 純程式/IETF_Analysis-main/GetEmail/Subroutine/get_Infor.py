import requests
import pandas as pd
from bs4 import BeautifulSoup

# ====== 擷取 "主題、寄件人、日期、連結" 資料 ======
# INPUT : "tar_link" => IETF Email Target link
# OUTPUT : df (Subject、From(sender)、Date、Link(mail))


def get_Information(tar_link, detail_link):
    r = requests.get(tar_link)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.findAll("div", class_="xtr")

    subj_list = []
    from_list = []
    date_list = []
    link_list = []
    for index in range(len(table)):
        try:
            subj_col = table[index].a.text  # 主題
            from_col = table[index].find(class_="xtd from-col").text  # 寄件人
            date_col = table[index].find(class_="xtd date-col").text  # 日期
            href_col = table[index].find(class_="xtd url-col d-none").text
            link_col = "https://mailarchive.ietf.org" + href_col  # 連結
            if link_col == detail_link:
                break
        except:
            subj_col = from_col = date_col = link_col = ""

        subj_list.append(subj_col)
        from_list.append(from_col)
        date_list.append(date_col)
        link_list.append(link_col)

    df = pd.DataFrame({"Subject": subj_list, "From": from_list,
                      "Date": date_list, "Link": link_list})
    return df
