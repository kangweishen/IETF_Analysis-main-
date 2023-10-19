import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

# === 擷取"收件人"資料 & 存檔===
IETF = pd.read_csv("IETF_WG_Link.csv", encoding="utf-8-sig")

# 計數器(工作組數量)
wg_count = len(IETF["link"])
run = 100 / wg_count

with tqdm(total=100) as pbar:
    for link_mail in range(wg_count):
        pbar.update(run)
        csv_name = "IETF_WG_Information_" + IETF["wg"][link_mail] + ".csv"
        csv_path = "get_information_csv/" + csv_name
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

        email_link = []
        link_count = len(df["Link"])
        if "Recipient" in df.columns:
            for link_index in range(link_count):
                if pd.isnull(df["Recipient"][link_index]):
                    email_link.append(df["Link"][link_index])
                else:
                    break
        else:
            email_link = df["Link"]

        count = len(email_link)
        if count == 0:
            continue
        print("\n正在擷取 %5d 位收件人至 %s" % (count, csv_name))

        recipients = []
        for url in email_link:
            try:
                res = requests.get(url + "#")
                soup = BeautifulSoup(res.text, "html.parser")
                content = soup.select("#msg-header > p")

                pattern = r"[^-]To:\s(.*)"
                matches = re.findall(pattern, content[0].text)
                matches = re.sub(r"\s<.*>", "", ''.join(matches))
                matches = re.sub(r'\"', "", matches)
                recipients.append(matches)
            except:
                recipients.append("")
                continue

        if "Recipient" in df.columns:
            for num in range(count):
                df.at[num, "Recipient"] = recipients[num]
        else:
            df.insert(5, "Recipient", recipients, True)
        df.to_csv(csv_path, encoding="utf-8-sig", index=False)
