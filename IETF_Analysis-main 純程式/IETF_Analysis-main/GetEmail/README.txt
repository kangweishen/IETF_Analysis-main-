此專案包含了 2個主程式 3個副程式

架構
GetEmail
d-----       __pycache__
d-----       chromedriver_win32
d-----       Subroutine
            d-----       __pycache__
            -a----       get_allGW_mail_content.py (主程式)
            -a----       get_IETF_WG_Link.py (副程式)
            -a----       get_Infor.py (副程式)
            -a----       get_MC.py (副程式)
-a----        __init__.py
-a----       main.py (主程式)
-a----       README.txt

主程式
main.py : 
    用來取得特定 WG 內的所有 email 連結，包括主題、寄件者、日期、信件連結
    再將上述內容各儲存於 WG 命名的 excel 中，同時將以上 excel 檔案，放於 get_information_csv 資料夾中

get_allGW_mail_content.py :
    擷取 各個 working group 的郵件內容，並將其存於 WG 命名的 excel 中(get_information_csv 資料夾內)

副程式
get_Infor.py :
    回傳帶有 WG 內的所有 email 連結，包括主題、寄件者、日期、信件連結的 df
    方法為 get_Information()

get_MC.py :
    回傳 WG 內的 Message 實際數量
    方法為 get_message_count()

get_IETF_WG_Link.py :
    取得的 各個 working group 的網址，並將 工作組名稱、連結、類別，儲存成excel
    名稱為 : IETF_WG_Link.csv
    方法為 get_IETF_WG_Link()

