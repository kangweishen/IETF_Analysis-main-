import re
import os
import time
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

import shutil
folderpath = "IETF工作組_基本資訊/IETF_Basic_Info"
csv_mailarchive = folderpath + "/mailarchive.csv"
if os.path.isfile(r"" + csv_mailarchive):
    df = pd.read_csv(csv_mailarchive)
    today = datetime.date.today()
    today_90 = today - datetime.timedelta(days=90)
    if df["Recorded Date"][0] < str(today_90):
        shutil.rmtree(folderpath)
    else:
        for num in range(len(df)):
            df.at[num, "Recorded Date"] = today
        df.to_csv(csv_mailarchive, encoding="utf-8-sig", index=False)
if os.path.isdir(folderpath) == False:
    os.mkdir(folderpath)
    print("已建立資料夾", folderpath)


def get_IETF_WG_Active():

    url = "https://datatracker.ietf.org/wg/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.findAll("tr")
    matches = []
    for index in table:
        match = re.findall(r'<a href="(\S*)">[\n\s]*(\S*)[\n\s]*', str(index))
        if match != "":
            matches.extend(match)
    active_wg = {"wg": [], "link": []}
    active_wg = pd.DataFrame(active_wg)
    for i in matches:
        new_row = pd.DataFrame(
            {"wg": [i[1]], "link": [url + i[1] + "/documents/"]})
        active_wg = pd.concat([active_wg, new_row], ignore_index=True)
    active_wg.to_csv(folderpath + "/IETF_WG_Active.csv",
                     encoding="utf-8", index=False)


def get_IETF_WG_Link():

    r = requests.get("https://mailarchive.ietf.org/arch/browse/")
    soup = BeautifulSoup(r.text, "html.parser")

    inactive = soup.find_all("div", id="inactive-lists")
    active = soup.find_all("div", id="active-lists")
    re_link = re.compile(r'href="([^"]*)"')
    inactive_list = re_link.findall(str(inactive))
    active_list = re_link.findall(str(active))

    re_name = re.compile(r'/arch/browse/([^/]*)/')
    active_name = re_name.findall(str(active_list))
    inactive_name = re_name.findall(str(inactive_list))

    status_list = []
    for i in range(0, len(active_list)):
        status_list.append("active")
        active_list[i] = "https://mailarchive.ietf.org" + active_list[i]
    for i in range(0, len(inactive_list)):
        status_list.append("inactive")
        inactive_list[i] = "https://mailarchive.ietf.org" + inactive_list[i]

    link_list = active_list + inactive_list
    name_list = active_name + inactive_name

    df = pd.DataFrame(
        {"wg": name_list, "link": link_list, "status": status_list})
    df = df.drop(0, axis=0)
    df.to_csv(folderpath + "/IETF_WG_Link.csv", encoding="utf-8", index=False)


def get_WG_About(wg_name):

    data = Name = Chairs = ""
    url = "https://datatracker.ietf.org/wg/" + wg_name + "/about/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    data = soup.findAll("tbody", class_="meta border-top")

    # WG Name
    Name = data[0].select("tr")[0].select("th")[2].text

    # Personnel Chairs: cbor, 6man, intarea, detnet, lake
    _chair = data[1].select("tr")[0]
    matches = re.findall(r'">(.*)</a>', str(_chair))
    Chairs = ", ".join(matches)

    time.sleep(0.5)
    return Name, Chairs


def get_WG_Documents(wg_name):

    url = "https://datatracker.ietf.org/wg/" + wg_name + "/documents/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # Active Internet-Drafts Numbers
    pattern = r"Active Internet-Draft[s]?\s\((\d+)\shit[s]?\)"
    matches = re.findall(pattern, str(soup))
    hit = "".join(matches)
    if hit == "":
        hit = "0"

    # Latest Draft Name & Date
    matches = []
    for index in range(1, int(hit)+1):
        data = soup.select(
            "tbody:nth-child(3) > tr:nth-child(" + str(index) + ")")
        pattern = r'(\S*)[\s\n]*</a>\n<br/>\n<b>(.*)</b>\n</div>\n</td>\n<td class="bg-transparent">[\s\n]*(\S*)[\s\n]*<'
        match = re.findall(pattern, str(data))
        if match[0][2] == "":
            pattern2 = r"(\S*)[\s\n]*</a>\n<br/>\n<"
            match2 = re.findall(pattern2, str(data))
            my_list = list(match[0])
            my_list[2] = match2[1]
            match[0] = tuple(my_list)
        matches.extend(match)
    if hit == "0":
        matches.append(("", "", ""))

    list4 = [matches[0][0], matches[0][1], matches[0][2]]

    time.sleep(0.5)
    return hit, list4


def get_WG_Meetings(wg_name):

    url = "https://datatracker.ietf.org/wg/" + wg_name + "/meetings/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.findAll("tbody")

    pattern = r"[\s\n]*(.*)[\s\n]*</td>\n<td>[\s\n]*(.*)[\s\n]*</td>\n<td>\n</td>\n<td>[\s\n]*(.*)[\s\n]*</td>"
    matches = re.findall(pattern, str(table))
    for i in range(len(matches)):
        match = re.findall(r"<i>(.*)</i>", matches[i][1])
        if match:
            demo_list = list(matches[i])
            demo_list[1] = match[0]
            matches[i] = tuple(demo_list)
    matches.append(("", "", ""))

    today = str(datetime.date.today())
    future = past = 0
    count = len(matches)
    for index in range(count):
        if matches[index][1] == "Cancelled":
            continue
        if today > matches[index][1]:
            future = count-1 if future == past else index-past
            break  # Future Meetings
        elif today < matches[index][1]:
            past = index + 1  # Past Meetings (within the last four years)
        elif today == matches[index][1]:
            future += 1
            past += 1  # Meetings in progress

    list5 = [matches[future][0], matches[future][1], matches[future][2]]
    list6 = [matches[past][0], matches[past][1], matches[past][2]]

    time.sleep(0.5)
    return list5, list6


def get_WG_Mail_Archive(wg_name):

    url = "https://mailarchive.ietf.org/arch/browse/" + wg_name + "/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    data = soup.findAll("div", class_="xtr")[0]
    if data.text == "No results found":
        subj = "No results found"
        form = date = ""  # iad20
    else:
        subj = data.find("span").text
        form = data.find("div", class_="xtd from-col").text
        date = data.find("div", class_="xtd date-col").text

    r = requests.get(url + "?qdr=m")
    soup = BeautifulSoup(r.text, "lxml")
    count = soup.select_one("#message-count").text
    today = str(datetime.date.today())

    list7 = [subj, form, date]
    list8 = [count, today]

    time.sleep(0.5)
    return list7, list8


csv_datatracker = folderpath + "/datatracker.csv"
csv_IETF_WG_Active = folderpath + "/IETF_WG_Active.csv"
if os.path.isfile(r"" + csv_IETF_WG_Active) == False:
    get_IETF_WG_Active()
    IETF_WG_Active = pd.read_csv(csv_IETF_WG_Active)
    IETF_WG_Active["wg"].to_csv(csv_datatracker, index=False)
datatracker = pd.read_csv(csv_datatracker)

# ===================  擷取工作組全名 主持人名稱 ===================
if "1.WG Name" not in datatracker.columns:
    print("正在 擷取 工作組全名 主持人名稱 中")

    Name = []
    Chairs = []

    for wg in datatracker["wg"]:
        x, y = get_WG_About(wg)
        Name.append(x)
        Chairs.append(y)

    datatracker.insert(1, "1.WG Name", Name, True)
    datatracker.insert(2, "2.Personnel Chairs", Chairs, True)
    datatracker.to_csv(csv_datatracker, encoding="utf-8-sig", index=False)

    print("擷取 工作組全名 主持人名稱 完成")

# =================== 擷取 最新草案更新名稱&日期 ===================
if "3.Active Internet-Drafts" not in datatracker.columns:
    print("正在 擷取 最新草案 更新名稱 & 日期 中")

    Number = []
    Drafts = {"Name": [], "Tittle": [], "Date": []}
    Drafts = pd.DataFrame(Drafts)

    for wg in datatracker["wg"]:
        x, y = get_WG_Documents(wg)
        Number.append(x)
        new_row = pd.DataFrame(
            {"Name": [y[0]], "Tittle": [y[1]], "Date": [y[2]]})
        Drafts = pd.concat([Drafts, new_row], ignore_index=True)

    datatracker.insert(3, "3.Active Internet-Drafts", Number, True)
    datatracker.insert(4, "4.Latest Draft Name", Drafts["Name"], True)
    datatracker.insert(5, "4.Latest Draft Tittle", Drafts["Tittle"], True)
    datatracker.insert(6, "4.Latest Draft Date", Drafts["Date"], True)
    datatracker.to_csv(csv_datatracker, encoding="utf-8-sig", index=False)

    print("擷取 最新草案 更新名稱 & 日期 完成")

# =================== 擷取 過去&未來的會議和日期(名稱&時間) ===================
if "5.Latest Future Meeting Name" not in datatracker.columns:
    print("正在 擷取 過去 & 未來 的 會議和日期(名稱&時間) 中")

    future = {"Name": [], "Date": [], "Week": []}
    future = pd.DataFrame(future)
    past = {"Name": [], "Date": [], "Week": []}
    past = pd.DataFrame(past)

    for wg in datatracker["wg"]:
        x, y = get_WG_Meetings(wg)
        row_x = pd.DataFrame({"Name": [x[0]], "Date": [x[1]], "Week": [x[2]]})
        future = pd.concat([future, row_x], ignore_index=True)
        row_y = pd.DataFrame({"Name": [y[0]], "Date": [y[1]], "Week": [y[2]]})
        past = pd.concat([past, row_y], ignore_index=True)

    datatracker.insert(7, "5.Latest Future Meeting Name", future["Name"], True)
    datatracker.insert(8, "5.Latest Future Meeting Date", future["Date"], True)
    datatracker.insert(9, "5.Latest Future Meeting Week", future["Week"], True)
    datatracker.insert(10, "6.Latest Past Meeting Name", past["Name"], True)
    datatracker.insert(11, "6.Latest Past Meeting Date", past["Date"], True)
    datatracker.insert(12, "6.Latest Past Meeting Week", past["Week"], True)
    datatracker.to_csv(csv_datatracker, encoding="utf-8-sig", index=False)

    print("擷取 過去 & 未來 的 會議和日期(名稱&時間) 完成")

csv_mailarchive = folderpath + "/mailarchive.csv"
csv_IETF_WG_Link = folderpath + "/IETF_WG_Link.csv"
if os.path.isfile(r"" + csv_IETF_WG_Link) == False:
    get_IETF_WG_Link()
    IETF_WG_Link = pd.read_csv(csv_IETF_WG_Link)
    IETF_WG_Link["wg"].to_csv(csv_mailarchive, index=False)
mailarchive = pd.read_csv(csv_mailarchive)

# =================== 擷取 最近的郵件 & 過去一個月郵件數量 ===================
if "7.Latest email Subject" not in mailarchive.columns:
    print("正在 擷取 最近的郵件 & 過去一個月郵件數量 中")

    email = {"Subject": [], "From": [], "Date": []}
    email = pd.DataFrame(email)
    record = {"Number": [], "Date": []}
    record = pd.DataFrame(record)

    for wg in mailarchive["wg"]:
        x, y = get_WG_Mail_Archive(wg)
        row_x = pd.DataFrame(
            {"Subject": [x[0]], "From": [x[1]], "Date": [x[2]]})
        email = pd.concat([email, row_x], ignore_index=True)
        row_y = pd.DataFrame({"Number": [y[0]], "Date": [y[1]]})
        record = pd.concat([record, row_y], ignore_index=True)

    mailarchive.insert(1, "7.Latest email Subject", email["Subject"], True)
    mailarchive.insert(2, "7.Latest email From", email["From"], True)
    mailarchive.insert(3, "7.Latest email Date", email["Date"], True)
    mailarchive.insert(4, "8.Past month Messages Number",
                       record["Number"], True)
    mailarchive.insert(5, "Recorded Date", record["Date"], True)
    mailarchive.to_csv(csv_mailarchive, encoding="utf-8-sig", index=False)

    print("擷取 最近的郵件 & 過去一個月郵件數量 完成")
