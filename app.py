from flask import Flask, request, abort, render_template, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from line_bot_api import *
from event.start_case import *
from event.emergency import *
from event.email import *
from event.system import *
from event.stu import *
from event.download import *
from event.FAQ import *
from event.check_letters_all import *
from event.letters_instructions import *
from event.location import *
from event.event_ad import *
from event.food_registration_sw import *
from event.food_registration_ch import *
from event.finished_booking import *
from event.call import *
from event.change_church import *

from Entity import *
import uuid
import time
import sched
import json
from dateutil import parser
from sqlalchemy import func

app.secret_key = ''

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '請登入！！！'

users_web = {'': {'password': ''}}

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    if user_id not in users_web:
        return

    user_web = User()
    user_web.id = user_id
    return user_web

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    user_id = request.form['user_id']
    if (user_id in users_web) and (request.form['password'] == users_web[user_id]['password']):
        user_web = User()
        user_web.id = user_id
        login_user(user_web)
        flash(f'{user_id} 歡迎回來！')
        return redirect(url_for('from_start'))

    flash('登入失敗')
    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id = current_user.get_id()
    logout_user()
    flash(f'{user_id}！歡迎下次再來！')
    return render_template('login.html') 


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/from_start")
@login_required
def from_start():
    return render_template("from_start.html")

@app.route("/users_list")
@login_required
def user_list():
    row = []
    col = []
    Users = users.query.order_by(users.Id).all ()
    for user in Users:
        col.append (user.Id)
        col.append (user.Display_name)
        col.append (user.Church)
        col.append (user.Region)
        row.append (col)
        col = []

    return render_template("users.html" , html_records = row)

@app.route("/letter_list")
@login_required
def letter_query():
    row = []
    col = []
    Letters = letter_list.query.order_by(letter_list.index).all ()
    for letter in Letters:
        col.append (letter.index)
        col.append (letter.church)
        col.append (letter.name)
        col.append (letter.sw)
        col.append (letter.persons)
        col.append (letter.title)
        col.append (letter.event)
        col.append (letter.notice)
        col.append (letter.due)
        col.append (letter.event_detail)
        col.append (letter.email_type)
        row.append (col)
        col = []

    return render_template("letter_list.html" , html_records = row)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id) 
    print ("user_id = " + user_id) 
    newcoming_text = profile.display_name + " 您好，\n歡迎使用芥菜種會專管小幫手，請使用手機操作下方服務選單說明。"
    newcoming_text2 = "如在操作上有問題或仍無法解決您的疑問，請直接私訊社工，感謝您的耐心。"
    text = [TextSendMessage (text = newcoming_text) , TextSendMessage (text = newcoming_text2)]
    uu_id = str(uuid.uuid4())
    new = db.session.query(func.max(users.Id).label('max_id')).one()
    print (new.max_id)
    Id = new.max_id + 1
    print (Id)
    insert_data = users( Id = Id , Uuid=uu_id , Userid=user_id , Display_name=profile.display_name , Church = None , State = 1 , IsFoodBank = None , FoodIndex = None , Region = None , Time = None)
    user = users.query.filter(users.Userid == user_id).first()
    if not user:
        db.session.add(insert_data)
        db.session.commit()
        print("DONE")
    else:
        print (user_id , " has already existed.")
    line_bot_api.link_rich_menu_to_user (user_id , "richmenu-8190b65e54fd3261bbd9d33dc951d1fe") 

    line_bot_api.reply_message(event.reply_token, text )

@handler.add(PostbackEvent)
def handle_post_message(event):
    print ("event =" , event)
    if event.postback.data == 'type' or event.postback.data == 'ask':
        text = emergency_postback(event.postback.data)
    elif event.postback.data.isdigit():
        text = start_case_postback_message(event.postback.data)
    elif event.postback.data == 'stepA' or event.postback.data == 'stepB':
        text = email_postback_message(event.postback.data)
    elif event.postback.data == 'data_fix' or event.postback.data == 'data_send' or event.postback.data == 'data_add':
        text = food_postback (event , event.source.user_id)
    elif event.postback.data == 'data_booking':
        text = booking_postback (event , event.source.user_id)
    elif event.postback.data == 'church_send' or event.postback.data == 'church_fix':
        text = ending_check (event , event.source.user_id)
 
    line_bot_api.reply_message(event.reply_token , text)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id) 
    new = db.session.query(func.max(users.Id).label('max_id')).one()
    Id = new.max_id + 1
    print (Id)
    uu_id = str(uuid.uuid4())
    insert_data = users( Id = Id , Uuid=uu_id , Userid=user_id , Display_name=profile.display_name , Church = None , State = 1 , IsFoodBank = None , FoodIndex = None , Region = None , Time = None)
    user = users.query.filter(users.Userid == user_id).first()
    if not user:
        db.session.add(insert_data)
        db.session.commit()
        print("DONE")
    print (user_id , " has already existed.")
   
    user_id = event.source.user_id

    if event.message.text == '社工專用':
        text = "✴️ 查詢教會信件：請輸入'信件查詢A'\n✴️ 查詢教會帳號密碼：請輸入'帳號密碼'\n✴️ 查詢北區服務中心地址：請輸入'交通資訊'。\n✴️ 物資登記相關說明：請輸入'物資相關說明'"
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = text))
#    elif event.message.text == '帳號密碼':
#        ask_account (event , user_id)
    elif event.message.text == '信件查詢A':
        check_letters (event , user_id)
    elif event.message.text == '信件查詢':
        check_letters_usual (event , user_id)
    elif event.message.text == '信件撰寫說明':
        letters_instructions (event)
    elif event.message.text == '近期活動':
        event_ad (event)
    elif event.message.text == '開案說明':
        start_case_event(event)
    elif event.message.text == '急難申請說明':
        emergency_event(event)
    elif event.message.text == '專管管理':
        change_church_event (event , user_id)
    elif event.message.text == '感謝/歡迎信email寄送說明':
        email_event(event)
    elif event.message.text == '助學金申請說明':
        stu_event(event)
    elif event.message.text == '三分量表說明':
        FAQ_event(event)
    elif event.message.text == '物資相關說明':
        user = users.query.filter(users.Userid == user_id).first()
        if user.State > 1:
            text = """🔵for 社工：
🔹指令：開放物資登記/關閉物資登記/物資一覽表/FoodBankRecovery
🔹指令說明：
 1️⃣ 開放物資登記：僅用於初次輸入物資資料使用。
⛔️因會更動資料庫且不可逆，建議彼此協調好後再由一人使用就好⛔️
‼️ 教會登記的物資資料在輸入此指令後會全數刪除，請先將上次的登記資料下載，下載方式請洽宥徵‼️
 2️⃣ 關閉物資登記：清除所有物資資料並重置所有教會物資登記狀態。
 3️⃣ 物資一覽表：平常想看物資狀態時使用。
 4️⃣ FoodBankRecovery：使用後需輸入user_id以恢復教會登記物資功能，使用後會清楚該使用者登記之所有資料、並重置登記功能。
🔹所有社工均能使用物資開放功能，但因所有專管小幫手好友使用同一資料庫，開放/關閉請協調好由誰輸入。
🔹開放/關閉均不會通知教會(但關閉後會使教會無法登記物資)，請社工在群組上通知各教會開始/結束登記。
--------------------
🟠for 教會：
🔸指令：物資登記/登記結果
🔸指令說明：
 1️⃣ 物資登記：登記物資使用。
 2️⃣ 登記結果：限登記完成的教會使用。
‼️ 同教會彼此會繼續登記，如有人填到一半中斷，下次他想起可繼續填、或是同教會的人亦會從那個物資繼續。‼️
‼️ 每個品項登記時間為20秒內、登記完所有品項確認60秒內需送出，如超過時間則會清除所有紀錄，必須重新登記。‼️ """
            line_bot_api.reply_message (event.reply_token , TextSendMessage (text = text))
    elif event.message.text == '物資一覽表':
        user = users.query.filter(users.Userid == user_id).first()
        if user.State > 1:
            json_flex (event)
    elif event.message.text == '開放物資登記':
        user = users.query.filter(users.Userid == user_id).first()
        if user.State == 2:
            food_registrate.query.delete ()
            db.session.commit()
            food_nums = food_num.query.filter (food_num.index == 1).first ()
            if food_nums.num != 0:
                text = "‼️ 請先關閉現有物資登記再重新輸入資料‼️ "
            else:
                user.State = 11
                db.session.commit()
                print ("user.State: %d" % (user.State ))
                text = set_food_data1 (event)
            line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))
    elif event.message.text == '關閉物資登記':
        user = users.query.filter(users.Userid == user_id).first()
        if user.State > 1:
            close_food (event , user_id)
    elif event.message.text == '物資登記':
        user = users.query.filter(users.Userid == user_id).first()
        if user.IsFoodBank == 1:
            food_booking (event , user_id , user.IsFoodBank)
        else:
            text = "您已經登記過了喔！如要重新登記請聯絡社區師協助。"
            line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))
    elif event.message.text == '登記結果':
        user = users.query.filter(users.Userid == user_id).first()
        if user.IsFoodBank == 5:
            flex = js_flex_finished (event , user_id)
            line_bot_api.reply_message(event.reply_token, flex)
        else:
            text = "您尚未登記物資喔！"
            line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))
    elif event.message.text == 'FoodBankRecovery':
        user = users.query.filter(users.Userid == user_id).first()
        if user.State > 1:
            user.State = 15
            db.session.commit ()  
            line_bot_api.reply_message (event.reply_token , TextSendMessage (text = '請輸入您要重啟登記功能的user_id：（先打給我好了👌）'))
    elif event.message.text == '相關表單下載':
        download_event(event)
    elif event.message.text == 'call_test':
        flex = call (event)
        line_bot_api.reply_message(event.reply_token, flex)
    elif event.message.text == '系統網址':
        system_event(event)
    elif event.message.text == '交通資訊':
        location (event)
#    elif event.message.text == '教會名稱查詢':
#        check_letters (event , user_id)
    elif event.message.text == '個案管理p.1':
        line_bot_api.link_rich_menu_to_user (user_id , "richmenu-84d7f90887b1ece1eb2c2c7d6d7985b0")
    elif event.message.text == '個案管理p.2':
        line_bot_api.link_rich_menu_to_user (user_id , "richmenu-cc77b263b47bbdedf9076ec937ef13e2")
    elif event.message.text == '回到首頁':
        line_bot_api.link_rich_menu_to_user (user_id , "richmenu-8190b65e54fd3261bbd9d33dc951d1fe") 
    elif event.message.text == '信件通知推播':
        user = users.query.filter(users.Userid == user_id).first()
        if user.State == 2:
            user.State = 4
            db.session.commit()
            line_bot_api.reply_message (event.reply_token , TextSendMessage (text = '請輸入密碼： '))
    elif event.message.text == '我愛你':
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = '耶穌愛你'))
    else:
        user = users.query.filter(users.Userid == user_id).first()
        if user.State > 10:
            food_conversation (event , user_id , user.State)
        elif user.State > 2 and user.State < 11:
            check_state (event , user_id , user.State)
        elif user.IsFoodBank > 1 and user.IsFoodBank != 5:
            print (user.IsFoodBank)
            user = users.query.filter(users.Userid == user_id).first()
            if event.message.text.isdigit ():
                food_booking (event , user_id , user.IsFoodBank)
            else:
                line_bot_api.reply_message (event.reply_token , TextSendMessage (text = "輸入錯誤！請重新輸入阿拉伯數字！"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
