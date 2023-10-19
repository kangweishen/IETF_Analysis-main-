import requests
from bs4 import BeautifulSoup
import re

# ====== 截取 "郵件數量" 資料 ======
# INPUT : "tar_link" => IETF Email Target link
# OUTPUT : (INT) Messages Number


def get_message_count(tar_link):
    # 取得 Messages 的總數量
    r = requests.get(tar_link)
    # 將此頁面的 HTML GET 下來

    html_Str = r.text
    # 變成 text 形式

    soup = BeautifulSoup(html_Str, "html.parser")
    # 以 Beautiful Soup 解析 HTML 程式碼

    count_text = soup.find(id="message-count").get_text()
    # 找出 Messages 數量的網頁元素資料的 text

    re_num = re.compile(r'\d+')
    # 正規表達式取出純數字的部分

    count_num = re_num.search(count_text).group()
    # 執行數字取出

    count_num = int(count_num)

    return count_num
