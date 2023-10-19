import os
import shutil
# == 刪除處理資料用excel檔案，減少壓縮大小 ==


def shutilpathin(shutilpath):
    if (os.path.isdir(shutilpath)) == True:
        shutil.rmtree(shutilpath)


def ospathin(ospath):
    if (os.path.isdir(ospath)) == True:
        os.remove(ospath)


shutilpath = ["get_information_csv", "get_email_amount_csv/Category",
              "get_subject_csv/Category", "IETF工作組_基本資訊/IETF_Basic_Info"]
ospath = ["IETF_WG_Link.csv", "mailingLists.csv"]

for i in range(len(shutilpath)):
    shutilpathin(shutilpath[i])

for j in range(len(ospath)):
    shutilpathin(ospath[j])

print("移除完成可以壓縮")
