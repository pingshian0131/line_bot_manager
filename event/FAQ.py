from line_bot_api import *

def FAQ_event (event):
        aae = """連結：https://donation.mustard.org.tw/MustardSurvey/Survey.aspx"""                    
        aaf = """1.電子郵件輸入您或教會的，不會寄信，只是作為辨識使用
2.訪談對象是照顧者，請填寫訪談對象的資料而非孩子，之後會有欄位請您填寫孩子姓名
3.戶號：需系統上填寫過第一次資料後右上方才會出現，第一次案家填寫時請案家填寫孩子的身分證字號。
***剛開案只要填完第一和第二面向就好(經濟和居住狀況)，剩下的半年到一年內填完就好***"""
        text = [TextSendMessage(text = aae) , TextSendMessage(text = aaf)]
        line_bot_api.reply_message(event.reply_token, text)

