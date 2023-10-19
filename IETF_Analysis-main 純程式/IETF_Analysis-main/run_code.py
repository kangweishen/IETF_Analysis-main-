import sys
import os
import nltk
nltk.download("punkt")

current_path = os.getcwd()
print(current_path)
os.chdir(current_path)
print(sys.executable)
# VScode 環境建置使用的 python.exe 所在位置
side = sys.executable  # "C:/Python39/python.exe"

cmd = "pip install -r requirements.txt"
os.system(cmd)  # python套件安裝
print("python套件安裝完成")

if (os.path.isdir("sqlite3")) == False:
    print("無資料庫")
else:
    cmd = side + ' readSQL.py'
    os.system(cmd)  # 擷取 IETF工作組 相關資料
    print("讀取資料庫 完成")

getInformation = input("是否擷取最新資料(Y/n):")
if getInformation == "Y":
    print("擷取 IETF工作組 相關資料 (get_IETF_imformation.py) 預計25分鐘")
    cmd = side + ' GetEmail/get_IETF_imformation.py'
    os.system(cmd)  # 擷取 IETF工作組 相關資料
    print("擷取 IETF工作組 相關資料 完成")

    print("擷取 IETF工作組 郵件內容 (get_allGW_mail_content.py) 預計4小時")
    cmd = side + ' GetEmail/Subroutine/get_allGW_mail_content.py'
    os.system(cmd)  # 擷取 IETF工作組 郵件內容
    print("擷取 IETF工作組 郵件內容 完成")

    print("擷取 IETF工作組 郵件收件人 (catch_recipient.py) 預計3.5小時")
    cmd = side + ' 郵件收件人/catch_recipient.py'
    os.system(cmd)  # 擷取 IETF工作組 郵件收件人
    print("擷取 IETF工作組 郵件收件人 完成")

    print("郵件 收件 寄件人 數量統計圖 (email_amount.py) 預計13分鐘")
    cmd = side + ' 郵件收件人/email_amount.py'
    os.system(cmd)  # 郵件 收件 寄件人 數量統計圖
    print("郵件 收件 寄件人 數量統計圖 完成")

    print("將 IETF工作組 郵件分類 並 統計作圖 (get_subject_Classification.py) 預計10分鐘")
    cmd = side + ' 郵件分類處理/get_subject_Classification.py'
    os.system(cmd)  # 將 IETF工作組 郵件分類 並 統計作圖
    print("將 IETF工作組 郵件分類 並 統計作圖 完成")

    print("將 IETF工作組 郵件依月分數量 建立時間軸 (timeline.py) 預計3分鐘")
    cmd = side + ' 郵件時軸/timeline.py'
    os.system(cmd)  # 將 IETF工作組 郵件依月分數量 建立時間軸
    print("將 IETF工作組 郵件依月分數量 建立時間軸 完成")

    print("擷取 工作組基本資料 (IETF_Basic_info.py)")
    cmd = side + ' IETF工作組_基本資訊/IETF_Basic_info.py'
    os.system(cmd)  # 擷取 工作組基本資料
    print("擷取 工作組基本資料 完成")

    print("擷取 郵件工作組介紹資料 (mailingLists.py)")
    cmd = side + ' 郵件組別介紹/mailingLists.py'
    os.system(cmd)  # 擷取 郵件工作組介紹資料
    print("擷取 郵件工作組介紹資料 完成")

saveInformation = input("是否儲存資料進資料庫(Y/n):")
if saveInformation == "Y":
    print("建立資料庫儲存資料中 (saveSQL.py)")
    cmd = side + ' saveSQL.py'
    os.system(cmd)
    cmd = side + ' saveSQL_all.py'
    os.system(cmd)  # 建立資料庫 儲存資料
    print("資料儲存 完成")

print(" 儀錶板展示 (main.py)")
cmd = 'streamlit run main.py'
os.system(cmd)  # 將 整理出來的結果 上傳到網頁上
