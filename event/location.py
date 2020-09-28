from line_bot_api import *

def location (event):
    
    text =""" 北區服務中心 個案管理師 (社工員)

電話：02-25974868分機2510

傳真：02-25975028
地址：台北市中山區雙城街49巷6-1號
官網： http://www.mustard.org.tw/
臉書： http://zh-tw.facebook.com/ms1952/"""

    line_bot_api.reply_message(event.reply_token,LocationSendMessage(title='基督教芥菜種會北區服務中心', address='台北市中山區雙城街49巷6-1號', latitude=25.068190, longitude=121.524700))

