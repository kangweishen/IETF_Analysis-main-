import csv
import time
import pandas as pd
import streamlit as st
from BM25.BM03 import *
from googletrans import Translator
from TFIDF.tfidf_wordcloud import *

st.set_page_config(
    page_title="IETF工作組郵件儀表板",
    page_icon="random",
    layout="wide",  # 網頁大小
    initial_sidebar_state="expanded"  # 側邊欄是否打開
)
# 選項內容配置
switch = "首頁"
SelectOptions = ["首頁", "功能選擇", "專題製作團隊"]
SelectFunction = ["熱門工作組排名", "目前活躍工作組-基本資訊", "參與者", "矚目主題 TOP10", "關鍵訊息"]
SelectFunctionFollower = ["參與者郵件數量排名、分布圖", "透過郵件收寄者 查看郵件內容"]
SelectFunctionKeymassege = ["關鍵字文字雲", "關鍵字查詢相關郵件"]

# (製作團隊)
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f"目前進度 {i+1} %")
    bar.progress(i + 1)
    time.sleep(0.01)

with open("IETF_WG_Link.csv", "rt", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    SelectIETFGroup = [row_wg["wg"] for row_wg in reader]

# 網頁內容配置
# ================================================================================================
switch = st.sidebar.selectbox("頁面選擇", SelectOptions)
"目前位置：", switch
# ================================================================================================
if switch == "首頁":

    st.title("初新者輕鬆接觸 IETF")
    st.subheader(
        "由於IETF網站資料內容複雜,於是我們將其擷取整理後呈現,希望能透過這種方式讓初新者能夠輕鬆地對IETF工作組有初步認識")
    st.image("https://blog.apnic.net/wp-content/uploads/2016/04/ietf_logo_blog.gif")
    note = ["IETF 官網: https://www.ietf.org/",
            "IETF Datatracker: https://datatracker.ietf.org/",
            "IETF 郵件: https://mailarchive.ietf.org/arch/",
            "IETF 資訊網站(TWINC): https://ietf.twnic.tw/"]
    expander = st.expander("參考網站")
    expander.write("\n\n".join(note))

# ================================================================================================
elif switch == "功能選擇":

    df_datatracker = pd.read_csv(
        "IETF工作組_基本資訊/IETF_Basic_Info/datatracker.csv", encoding="utf-8-sig")  # 讀取 工作組 基本資訊
    df_mailarchive = pd.read_csv(
        "IETF工作組_基本資訊/IETF_Basic_Info/mailarchive.csv", encoding="utf-8-sig")  # 讀取 信件 基本資訊
    df_IETFmailGroup = pd.read_csv("mailingLists.csv", encoding="utf-8-sig")
    select_function = st.sidebar.selectbox("選擇功能", SelectFunction)
    "功能：", select_function
    select_IETFGroup = st.sidebar.selectbox("選擇工作組？", SelectIETFGroup)

    # ================================================================================================
    if select_function == "熱門工作組排名":
        note = ["透過近期討論草案數量，判斷出近期熱門工作組，同時藉由輸入下限值排名", "不用以下內容定義熱門原因:", "1.郵件數量:其中混雜著各式各樣的郵件,有的甚至只是討論無關的私事或是公告訊息,無法客觀討論是否熱門",
                "2.RFC(定案)數量:有些工作組雖說定案數量多,但是實際討論的草案極少,此處僅能代表其工作組草案通過率高，無法判定其為熱門工作組", "3.關鍵字:無法得知IETF關鍵字搜尋頻率,且本程式僅作為新手入門統整平台無法統計造訪量", "4.參與度:僅能代表參與者踴躍程度", "5.會議名稱:僅能得知近期參與會議工作組"]
        expander = st.expander("查看功能簡介")
        expander.write("\n\n".join(note))
        DraftsNum = df_datatracker["3.Active Internet-Drafts"]
        Drafts = {"工作組": [], "草案數量": []}
        Drafts = pd.DataFrame(Drafts)
        type_keyword = st.text_input(label="輸入草案下限", value="0")
        if type_keyword:
            for i in range(len(DraftsNum)):
                if DraftsNum[i] >= int(type_keyword):
                    # countNo = countNo + 1
                    new_row = pd.DataFrame(
                        {"工作組": [df_datatracker["wg"][i]], "草案數量": [DraftsNum[i]]})
                    Drafts = pd.concat([Drafts, new_row], ignore_index=True)

        from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
        "熱門工作組排名(透過草案數量判斷)："
        Drafts = Drafts.sort_values(
            by=["草案數量"], ignore_index=True, ascending=False)
        AgGrid(pd.DataFrame(Drafts, columns=Drafts.columns),
               fit_columns_on_grid_load=True, height=400, theme='balham',)

    # ================================================================================================
    elif select_function == "目前活躍工作組-基本資訊":

        # SelectActiveIETFGroup = df_datatracker["wg"]
        expander = st.expander("查看功能簡介")
        expander.write("可以了解目前活躍的工作組基本資訊")
        try:
            # ================ 工作組縮寫 大標 ================
            st.title(select_IETFGroup)

            # ================ 工作組 是否存在於 df_datatracker ================
            wg_datatracker = df_datatracker[df_datatracker["wg"]
                                            == select_IETFGroup]
            if wg_datatracker.empty == False:

                # ================ 工作組全名 ================
                select_IETFmailGroup = str(select_IETFGroup).capitalize()
                wg_IETFmailGroup = df_IETFmailGroup[df_IETFmailGroup["List"]
                                                    == select_IETFmailGroup]
                if wg_IETFmailGroup.empty == False:
                    st.subheader("郵件工作組的分類介紹")
                    "郵件工作組名稱：", select_IETFmailGroup
                    mailGroupIntroduction = wg_IETFmailGroup["Description"]
                    translator = Translator()
                    result = translator.translate(
                        ("  ".join(mailGroupIntroduction.values)), dest="zh-tw").text
                    "郵件工作組介紹：", ("  ".join(mailGroupIntroduction.values)
                                 ), "(", result, ")"
                    mailGroupURL = wg_IETFmailGroup["Url"]
                    "如果想收到相關郵件，可以至以下網址訂閱：", ("  ".join(mailGroupURL.values))

                # ================ 工作組全名 副標 ================
                wgName = wg_datatracker["1.WG Name"]
                st.subheader(",".join(wgName))

                # ================ 工作組主導人印出 ================
                wgChairs = wg_datatracker["2.Personnel Chairs"]
                "工作組主導人：", (",".join(wgChairs))

                # ================ 活躍草案數 ================
                wgDraftsNum = wg_datatracker["3.Active Internet-Drafts"]
                "活躍草案數：", str(wgDraftsNum.values)

                # ================ 最近更新草案名稱 ================
                wgDraftsName = wg_datatracker["4.Latest Draft Name"]
                wgDraftsName1 = wg_datatracker["4.Latest Draft Tittle"]
                wgDraftsName2 = wg_datatracker["4.Latest Draft Date"]

                pdwgDraftsName = pd.DataFrame(wgDraftsName)
                pdwgDraftsName = pdwgDraftsName.fillna(0)

                if pdwgDraftsName.values == 0:
                    "最近更新草案：", "無"
                else:
                    "最近更新草案：", " < ", (",".join(wgDraftsName)
                                       ), " > ", (",".join(wgDraftsName1))
                    wgDraftsNameLink = "https://datatracker.ietf.org/doc/html/" + \
                        (",".join(wgDraftsName.values))
                    expander = st.expander("點擊查看草案連結...")
                    expander.write(wgDraftsNameLink)
                    # https://datatracker.ietf.org/doc/html/rfc9409
                    "更新時間：", (",".join(wgDraftsName2))

                # ================ 即將開始的會議 ================
                LatestFutureMeeting = wg_datatracker["5.Latest Future Meeting Name"]
                LatestFutureMeeting1 = wg_datatracker["5.Latest Future Meeting Date"]
                LatestFutureMeeting2 = wg_datatracker["5.Latest Future Meeting Week"]

                pdLatestFutureMeeting = pd.DataFrame(LatestFutureMeeting)
                pdLatestFutureMeeting = pdLatestFutureMeeting.fillna(0)

                if pdLatestFutureMeeting.values == 0:
                    "即將開始的會議：", "無"
                elif LatestFutureMeeting1.values == "Waiting for Scheduling":
                    "即將開始的會議：", ("".join(LatestFutureMeeting)
                                 ), ".", ("".join(LatestFutureMeeting1))
                else:
                    "即將開始的會議：", ("".join(LatestFutureMeeting)), ".", ("".join(
                        LatestFutureMeeting1)), "(", ("".join(LatestFutureMeeting2.values)), ")"

                # ================ 最近已結束的會議 ================
                LatestPastMeeting = wg_datatracker["6.Latest Past Meeting Name"]
                LatestPastMeeting1 = wg_datatracker["6.Latest Past Meeting Date"]
                LatestPastMeeting2 = wg_datatracker["6.Latest Past Meeting Week"]

                pdLatestPastMeeting = pd.DataFrame(LatestPastMeeting)
                pdLatestPastMeeting = pdLatestPastMeeting.fillna(0)

                if pdLatestPastMeeting.values == 0:
                    "最近已結束的會議：", "無"
                elif LatestPastMeeting1.values == "Cancelled":
                    "最近已結束的會議：", ("".join(LatestPastMeeting)
                                  ), ".", ("".join(LatestPastMeeting1))
                else:
                    "最近已結束的會議：", ("".join(LatestPastMeeting)), ".", ("".join(
                        LatestPastMeeting1)), "(", ("".join(LatestPastMeeting2.values)), ")"
            # ================ 工作組 郵件資訊 ================
            wg_mailarchive = df_mailarchive[df_mailarchive["wg"]
                                            == select_IETFGroup]
            LatestEmail = wg_mailarchive["7.Latest email Subject"]
            LatestEmail1 = wg_mailarchive["7.Latest email From"]
            LatestEmail2 = wg_mailarchive["7.Latest email Date"]
            PastMonthMessagesNumber = wg_mailarchive["8.Past month Messages Number"]
            RecordedDate = wg_mailarchive["Recorded Date"]
            st.subheader("工作組 郵件資訊")
            "最近的郵件標題：", (",".join(LatestEmail))
            "寄件人：", (",".join(LatestEmail1))
            "時間：", (",".join(LatestEmail2))
            "過去一個月郵件數量：", (",".join(PastMonthMessagesNumber))
            "程式最近一次更新時間：", (",".join(RecordedDate.values))
            "其郵件收送時軸："
            st.image("get_timeLine/timeLine_" + select_IETFGroup + ".png")

            # "所有資料 dataframe:"
            # df_datatracker
            # df_mailarchive

        except:
            "稍待片刻"

    # ================================================================================================
    elif select_function == "參與者":
        select_function_follower = st.sidebar.selectbox(
            "選擇功能", SelectFunctionFollower)

        # ================================================================================================
        if select_function_follower == "參與者郵件數量排名、分布圖":
            note = ["寄件者:可以得知為主動參與者，並推斷其為較為踴躍的參與者",
                    "收件者:可以推知其為工作組中較為重要的成員(如：主持人)", "長條圖:能清楚排名", "圓餅圖:能得知分布數量占比，證明重要度"]
            expander = st.expander("查看功能簡介")
            expander.write("\n\n".join(note))
            try:
                "參與討論者寄信數量排名:"
                st.image("get_email_amount_csv/sender_ChartBar/barChart_sender_" +
                         select_IETFGroup + ".png")
                "寄件者數量分布:"
                st.image("get_email_amount_csv/sender_ChartPie/pieChart_sender_" +
                         select_IETFGroup + ".png")
                "參與討論者收信數量排名:"
                st.image("get_email_amount_csv/recipient_ChartBar/barChart_recipient_" +
                         select_IETFGroup + ".png")
                "收件者數量分布:"
                st.image("get_email_amount_csv/recipient_ChartPie/pieChart_recipient_" +
                         select_IETFGroup + ".png")
            except:
                "稍待片刻"

        # ================================================================================================
        elif select_function_follower == "透過郵件收寄者 查看郵件內容":
            note = ["透過郵件收寄者分類圖功能得知重要收寄件者後,此處可以查看他們收送的郵件內容"]
            expander = st.expander("查看功能簡介")
            expander.write("\n\n".join(note))
            select_Who = st.selectbox("選擇收寄件者？", ["寄件者", "收件者"])
            if select_Who == "寄件者":
                selectSender = pd.read_csv(
                    "get_email_amount_csv/Category/email_amount_" + select_IETFGroup + ".csv", usecols=["From"], encoding="utf-8-sig")
                select_sender = st.selectbox("選擇寄件者？", selectSender)
                df_content = pd.read_csv(
                    "get_information_csv/IETF_WG_Information_" + select_IETFGroup + ".csv", encoding="utf-8-sig")
                senderContent = df_content[df_content["From"]
                                           == select_sender]["Content"]
                "寄件者撰寫過的郵件內容"
                count = 1
                senderdict = {}
                for i in senderContent:
                    senderdict[count] = i
                    count += 1
                select_num = st.selectbox("選擇第幾封？", list(senderdict.keys()))
                expander = st.expander("點擊查看郵件內容...")
                expander.write(senderdict[select_num])
            elif select_Who == "收件者":
                selectSender = pd.read_csv(
                    "get_email_amount_csv/Category/email_amount_" + select_IETFGroup + ".csv", usecols=["Recipient"], encoding="utf-8-sig")
                select_sender = st.selectbox("選擇收件者？", selectSender)
                df_content = pd.read_csv(
                    "get_information_csv/IETF_WG_Information_" + select_IETFGroup + ".csv", encoding="utf-8-sig")
                senderContent = df_content[df_content["Recipient"]
                                           == select_sender]["Content"]
                "收件者收到的郵件內容"
                count = 1
                senderdict = {}
                for i in senderContent:
                    senderdict[count] = i
                    count += 1
                select_num = st.selectbox("選擇第幾封？", list(senderdict.keys()))
                expander = st.expander("點擊查看全部內容...")
                expander.write(senderdict[select_num])

    # ================================================================================================
    elif select_function == "矚目主題 TOP10":
        note = ["長條圖: 能清楚得知被受關注的前十名主題為何", "圓餅圖: 可以了解前十名主題數量占比，進而比較個別主題討論度"]
        expander = st.expander("查看功能簡介")
        expander.write("\n\n".join(note))
        try:
            "廣受矚目的郵件主題 TOP10："
            st.image("get_subject_csv/ChartBar/barChart_" +
                     select_IETFGroup + ".png")
            "TOP10 主題占比："
            st.image("get_subject_csv/ChartPie/pieChart_" +
                     select_IETFGroup + ".png")
        except:
            "稍待片刻"

    # ================================================================================================
    elif select_function == "關鍵訊息":
        select_function_keymassege = st.sidebar.selectbox(
            "選擇功能", SelectFunctionKeymassege)

        # ================================================================================================
        if select_function_keymassege == "關鍵字文字雲":
            note = ["可以利用文字雲探索關鍵字後，並能於工作組個別主題中查詢符合關鍵字匹配郵件內容", "若有不懂的英文詞彙可於翻譯處翻譯"]
            expander = st.expander("查看功能簡介")
            expander.write("\n\n".join(note))
            skip = 0
            try:
                Subject_list = Select_Subject(select_IETFGroup)
                ChooseSubject = st.selectbox("想看什麼類別？", Subject_list)
                type_keyword = st.text_input(label="輸入想翻譯文字內容", value="")

                if type_keyword:
                    translator = Translator()
                    result = translator.translate(
                        type_keyword, dest="zh-tw").text
                    "翻譯結果：", result

                else:
                    TFIDF(select_IETFGroup, ChooseSubject)
                "此郵件類別產生的文字雲如下:"
                st.image("tfidf_wordcloud.png")

            except:
                "無法產生關鍵字文字雲,請擴充該類別資料後再嘗試"

        # ================================================================================================
        elif select_function_keymassege == "關鍵字查詢相關郵件":
            note = ["可以利用關鍵字於工作組個別主題中查詢匹配郵件內容、其相關性分數(越高分其相關性越高)、郵件摘要"]
            expander = st.expander("查看功能簡介")
            expander.write("\n\n".join(note))
            try:
                "工作組：", select_IETFGroup
                "剛剛得到的關鍵字文字雲："
                st.image("tfidf_wordcloud.png")
                type_keyword = st.text_input(label="在sidebar輸入一些文字", value="")
                if type_keyword:
                    BM(select_IETFGroup, type_keyword)
                    df_BM25_output = pd.read_csv(
                        "BM25/BM25_output.csv", usecols=["Match No.", "score", "Mail Subject"], encoding="utf-8")
                    "關鍵字搜尋結果如下："
                    st.dataframe(df_BM25_output)

                    df_BM25_MailContent = pd.read_csv(
                        "BM25/BM25_output.csv", usecols=["Mail Content"], encoding="utf-8")
                    list_of_BM25_MailContent = df_BM25_MailContent["Mail Content"].tolist(
                    )
                    str_of_BM25_MailContent = " ".join(
                        list_of_BM25_MailContent)
                    "匹配的郵件內容："
                    expander = st.expander("點擊查看全部內容...")
                    expander.write(str_of_BM25_MailContent)

                    # 郵件摘要展示
                    df_BM25_MailSummary = pd.read_csv(
                        "BM25/BM25_summary.csv", usecols=["Mail summary"], encoding="utf-8")
                    list_of_BM25_MailSummary = df_BM25_MailSummary["Mail summary"].tolist(
                    )
                    str_of_BM25_MailSummary = "\n\n".join(
                        list_of_BM25_MailSummary)
                    "郵件摘要"
                    expander = st.expander("點擊查看全部內容...")
                    expander.write(str_of_BM25_MailSummary)
                    expander = st.expander("點擊查看摘要翻譯...")
                    translator = Translator()
                    result = translator.translate(
                        str_of_BM25_MailSummary, dest="zh-tw").text
                    expander.write(result)
                else:
                    "稍待片刻"
            except:
                "無匹配資料，請換關鍵字搜尋"

# ================================================================================================
elif switch == "專題製作團隊":

    note = ["專題製作團隊名單：", "張祐維", "吳永堉", "陳昱睿",
            "黃紀維", "鍾甯云", "李愛葳", "林品伃", "康維珅"]
    st.write("\n\n".join(note))
    "指導教授: 林正偉教授"
