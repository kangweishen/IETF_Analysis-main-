import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# === 擷取"工作組名稱介紹"資料 ===
url = "https://www.ietf.org/mailman/listinfo/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
table = soup.findAll("tr")

matches = []
for item in table:
    match = re.findall(
        r'<strong>(\S*)</strong></a></td>\n<td>(.*)</td>', str(item))
    if match != "":
        matches.extend(match)

data = {"List": [], "Description": [], "Url": []}
data = pd.DataFrame(data)
for i in matches:
    row = pd.DataFrame({"List": [i[0]], "Description": [
                       i[1]], "Url": [url + i[0]]})
    data = pd.concat([data, row], ignore_index=True)
data.to_csv("mailingLists.csv", encoding="utf-8", index=False)
