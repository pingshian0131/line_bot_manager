from line_bot_api import *
from Entity import *
from sqlalchemy import func
from datetime import datetime 
from event.finished_booking import *

import json

fix = 1

bubble = """{
  "type": "bubble","""
header = """
  "header": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "text",
        "text": "物",
        "size": "xxl",
        "align": "center",
        "color": "#00AA00",
        "weight": "bold"
      },
      {
        "type": "text",
        "text": "資",
        "weight": "bold",
        "size": "xxl",
        "align": "center",
        "color": "#00AA00"
      },
      {
        "type": "text",
        "text": "登",
        "weight": "bold",
        "size": "xxl",
        "align": "center",
        "color": "#00AA00"
      },
      {
        "type": "text",
        "text": "記",
        "weight": "bold",
        "size": "xxl",
        "align": "center",
        "color": "#00AA00"
      }
    ]
  },"""
body1 = """
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "目前開放物資如下",
            "size": "md",
            "color": "#FF8888",
            "align": "center",
            "style": "italic",
            "wrap": true
          },
          {
            "type": "text",
            "text": "請按下方按鈕開始登記",
            "size": "md",
            "color": "#FF8888",
            "align": "center",
            "style": "italic",
            "wrap": true
          },
          {
            "type": "text",
            "text": "如有不需要的項目請填0",
            "size": "md",
            "color": "#FF8888",
            "align": "center",
            "style": "italic",
            "wrap": true
          },
          {
            "type": "text",
            "text": "此頁顯示結果僅供參考，實際仍以最後是否完成登記為主。",
            "size": "md",
            "color": "#FF8888",
            "align": "center",
            "style": "italic",
            "wrap": true
          },
          {
            "type": "spacer",
            "size": "xxl"
          }
        ]
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "margin": "md",
            "size": "md",
            "flex": 1,
            "color": "#BEBEBE",
            "align": "start",
            "contents": [],
            "text": "編號"
          },
          {
            "type": "text",
            "margin": "md",
            "size": "md",
            "flex": 2,
            "color": "#BEBEBE",
            "align": "center",
            "contents": [],
            "text": "品項"
          },
          {
            "type": "text",
            "contents": [],
            "color": "#BEBEBE",
            "flex": 2,
            "align": "center",
            "text": "總數"
          },
          {
            "type": "text",
            "contents": [],
            "color": "#BEBEBE",
            "flex": 1,
            "align": "center",
            "text": "單位",
            "size": "md"
          }
        ],
        "flex": 1
      },
      {
        "type": "separator",
        "color": "#84C1FF",
        "margin": "lg"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": ["""
separator = """,
          {
            "type": "separator",
            "color": "#84C1FF",
            "margin": "md"
          },"""
body2 = """
        ]
      }
    ]
  },"""

def make_footer (index):
    foods = food.query.filter(food.index == index).first()
    footer = """
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "開始登記",
          "data": "data_booking",
          "displayText": "請輸入您要登記""" + foods.item + """的數量：(ex, 2)"
        },
        "height": "sm",
        "style": "primary",
        "color": "#FF0000"
      }
    ]
  }
}"""
    return footer

def make_body_element (index):
    foods = food.query.filter(food.index == index).first()
    item = foods.item
    total = foods.total
    unit = foods.unit
    Max = foods.Max 

    body_element = """
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "size": "md",
                "flex": 1,
                "align": "center",
                "contents": [],
                "color": "#BEBEBE",
                "text": """ + '"' + str(index) + '"' + """,
                "weight": "bold"
              },
              {
                "type": "text",
                "margin": "md",
                "size": "md",
                "flex": 2,
                "color": "#46A3FF",
                "align": "center",
                "contents": [],
                "wrap": true,
                "text": """ + '"' + item + '"' + """,
                "weight": "bold"
              },
              {
                "type": "text",
                "margin": "md",
                "size": "md",
                "flex": 2,
                "color": "#46A3FF",
                "align": "center",
                "contents": [],
                "text": """ + '"' + str(total) + '"'+ """,
                "weight": "bold"
              },
              {
                "type": "text",
                "contents": [],
                "color": "#BEBEBE",
                "flex": 1,
                "align": "center",
                "text": """ + '"' + unit + '"' + """
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "margin": "md",
                "size": "sm",
                "flex": 3,
                "color": "#D0D0D0",
                "align": "center",
                "contents": [],
                "wrap": true,
                "text": "最多領取數量/教會"
              },
              {
                "type": "text",
                "margin": "md",
                "size": "md",
                "flex": 2,
                "color": "#46A3FF",
                "align": "center",
                "contents": [],
                "text": """ + '"' + str(Max) + '"' + """,
                "weight": "bold"
              },
              {
                "type": "text",
                "contents": [],
                "color": "#BEBEBE",
                "flex": 1,
                "align": "center",
                "text": """ + '"' + unit + '"' + """,
                "size": "md"
              }
            ]
          }"""
    return body_element 

index_s = []

def check_church (event , user_id):
    user = users.query.filter(users.Userid == user_id).first()
    church = user.Church 
    IsBooked = users.query.filter (users.Church == church).all ()
    result = 0
    a = 0
    for manager in IsBooked:
        if manager.IsFoodBank == 5:
            result = 1
        elif manager.IsFoodBank == 2:
            if manager.FoodIndex > a:
                a = manager.FoodIndex
    return result , a 

def booking_postback (event , user_id):
    result , max_food_index = check_church (event , user_id)
    user = users.query.filter(users.Userid == user_id).first()
#    if user.FoodIndex == 0:
#        return TextSendMessage (text = "您已經登記過了喔！")
    if result == 0:
        t_now = datetime.datetime.now ()
        t_record = user.Time 
        t_diff = t_now - t_record 
        if t_diff.seconds > 60:
            text = reset_food_booking (user_id)
            return TextSendMessage (text = text)
        user.Time = t_now.strftime ('%Y-%m-%d %H:%M:%S.%f')
        user.IsFoodBank = 2
        db.session.commit()
#        if max_food_index == 0:  ######## 沒有其他人填過
        foods = food.query.filter (food.index == user.FoodIndex).first ()
        return TextSendMessage (text = "最多只能登記 " + str(foods.Max) + foods.unit + " 喔！\n尚餘 " + str (foods.total) + foods.unit + " 喔！")
        
#        elif max_food_index > 0:   ######### 有其他人填過且填一半
#    elif result == 1:
#        return TextSendMessage (text = "您的教會已經登記過了喔！" )

def reset_food_booking (user_id):
    target = food_registrate.query.filter (food_registrate.userid == user_id).first ()
    if target != None:
        food_registrate.query.filter (food_registrate.userid == user_id).delete ()
    db.session.commit ()
    user = users.query.filter(users.Userid == user_id).first()
    user.IsFoodBank = 1
    user.FoodIndex = None
    db.session.commit ()
    text = "物資登記已逾時，請重新開啟物資登記程序。"
    return text 


def book_food (event , user_id):
    global index_s
    t_now = datetime.datetime.now()
    records = food_registrate.query.filter (food_registrate.userid == user_id).all ()
    print (records)
    if records != []:
        tmp = 0
        tt = ""
        for record in records:
            if record.index > tmp:
                tmp = record.index 
                tt = record.time.strftime ('%Y-%m-%d %H:%M:%S.%f') 
        t_record = datetime.datetime.strptime (tt , '%Y-%m-%d %H:%M:%S.%f')
        t_diff = t_now - t_record 
        if t_diff.seconds > 20:
            text = reset_food_booking (user_id)
            line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
            return 
    else:
        user = users.query.filter(users.Userid == user_id).first()
        t_record = user.Time
        t_diff = t_now - t_record 
        if t_diff.seconds > 20:
            text = reset_food_booking (user_id)
            line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
            return 
       
    user = users.query.filter(users.Userid == user_id).first()
    foods = food.query.filter (food.index == user.FoodIndex).first ()
    num = int (event.message.text)
    if foods.Max == 0:
        text = foods.item + "已經被登記完囉！"
        line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
        return 
    else:
        if num <= foods.Max and num >= 0:
            print ("index: %d , book_total: %d" % (user.FoodIndex , num))
            currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            food_registrate_s = food_registrate.query.filter (food_registrate.index == 1).with_for_update().scalar ()
            if food_registrate_s != None:
                food_index = db.session.query(func.max(food_registrate.index).label('max')).one()
                print (food_index)
                Max_id = food_index.max + 1
            else:
                Max_id = 1
            insert_data = food_registrate ( index = Max_id , time = currentTime , userid = user_id , item = foods.item , num = num , IsFinished = None) 
            db.session.add(insert_data)
            db.session.commit()
            index_s.pop (0)
        else:
            text = "最多只能登記" + str (foods.Max) + foods.unit + " 喔！\n尚餘 " + str (foods.total) + foods.unit + " 喔！"
            line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
            return 
    if index_s != []:
        user.FoodIndex = index_s[0]
        db.session.commit()
        foods = food.query.filter (food.index == user.FoodIndex).first ()
        text = "請輸入您要登記" + foods.item + "的數量：\n(最多 " + str (foods.Max) + foods.unit + " 尚餘 " + str (foods.total) + foods.unit + " 喔！)"
        line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text) )
    else:
        flex = js_flex_fix (event , user_id)
        line_bot_api.reply_message (event.reply_token, flex )
        user = users.query.filter(users.Userid == user_id).first()
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        user.Time = currentTime 
        user.IsFoodBank = 3
        user.FoodIndex = 0
        db.session.commit ()

fixed_item = ""

def fix_record1 (event , user_id):

    records = food_registrate.query.filter (food_registrate.userid == user_id).all ()
    items_index = []
    for record in records:
        item_record = food.query.filter (food.item == record.item).first ()
        items_index.append (item_record.index)

    if int (event.message.text) in items_index:
        target = food.query.filter (food.index == int (event.message.text)).first()
        user = users.query.filter(users.Userid == user_id).first()
        t_now = datetime.datetime.now()
        t_record = user.Time
        t_diff = t_now - t_record 
        if t_diff.seconds <= 60:
            user.Time = t_now.strftime('%Y-%m-%d %H:%M:%S.%f') 
            user.IsFoodBank = 4
            user.FoodIndex = target.index 
            db.session.commit ()
        else:
            text = reset_food_booking (user_id)
            line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
            return 
        text = "請輸入您要修改的 " + target.item + " 數量：\n(最多 " + str(target.Max) + target.unit + " 尚餘 " + str(target.total) + target.unit + " )"
    else:
        text = "輸入錯誤！請輸入正確項目代碼！"
    line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
        
def fix_record2 (event , user_id):
    global fixed_item 
    user = users.query.filter(users.Userid == user_id).first()
    target = food.query.filter (food.index == user.FoodIndex).first ()
    record = food_registrate.query.filter (food_registrate.item == target.item).first ()
    fixed_item = target.item 
    if int (event.message.text) <= target.Max and int (event.message.text) >= 0:
        t_now = datetime.datetime.now()
        t_record = user.Time 
        t_diff = t_now - t_record 
        if t_diff.seconds <= 60:
            record.num = int (event.message.text)
            db.session.commit ()    
            record.time = t_now.strftime('%Y-%m-%d %H:%M:%S.%f')
            user.IsFoodBank = 3
            db.session.commit ()
            flex = js_flex_fix (event , user_id)
            line_bot_api.reply_message (event.reply_token , flex)
        else:
            text = reset_food_booking (user_id)
            line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
            fixed_item = ""
    else:
        text = "輸入錯誤！請輸入正確的數量！\n" + "介於 " + str(target.Max) + " ~ 0 之間"
        line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
   

def ending_check (event , user_id):
    global fix , fixed_item 
    user = users.query.filter(users.Userid == user_id).first()
    if event.postback.data == 'church_send':
        t_now = datetime.datetime.now()
        if user.FoodIndex != 0:
            record = food_registrate.query.filter (food_registrate.item == fixed_item).first ()
            t_record = record.time 
            t_diff = t_now - t_record 
            if t_diff.seconds > 60:
                text = reset_food_booking (user_id)
                line_bot_api.reply_message (event.reply_token, TextSendMessage (text = text))
                fixed_item = ""
                return 

        user = users.query.filter(users.Userid == user_id).first()
        user.IsFoodBank = 5
        user.FoodIndex = 0
        db.session.commit ()
######## 將所有同教會的user鎖住 暫不使用此功能 #######
#        church_list = users.query.filter (users.Church == user.Church).all()
#        for church in church_list:
#            church.IsFoodBank = 5
#            church.FoodIndex = 0
#            db.session.commit ()

        finish_record = food_registrate.query.filter (food_registrate.userid == user_id).all ()
        for record in finish_record:
            foods = food.query.filter (food.item == record.item).with_for_update().first ()
            record.IsFinished = 1
            record.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            if foods.total < record.num:
                record.num = foods.total 
                db.session.commit () 
            foods.total -= record.num
            db.session.commit () 
        text = js_flex_finished (event , user_id)
        fix = 0
    elif event.postback.data == 'church_fix':
        if fix != 0:
            user = users.query.filter(users.Userid == user_id).first()
            currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            user.Time = currentTime 
            user.IsFoodBank = 3
            db.session.commit ()
            text = TextSendMessage (text = "請輸入欲修改項目編號：(ex , 1)")
        else: 
            text = TextSendMessage (text = "您已完成登記囉！無法修改，欲修改請洽社區師。")
    return text 


def json_flex_ch (event , user_id):
    global bubble , header , body1 , body2 , styles , separator 
    global index , index_s , fix 
    fix = 1 
    body_s = []
    index_s = []

    foods = food.query.order_by(food.index).all()
    for product in foods:
        if product.total > 0:
            print ("index: %d , element: %s" % (product.index , product.item))
            index_s.append (product.index)
            body_s.append (make_body_element (product.index))
            body_s.append (separator)
    body_s.pop ()
    print (index_s)
    result , max_food_index = check_church (event , user_id)
    print ("result: %d , max_food_index: %d" % (result , max_food_index))

    user = users.query.filter(users.Userid == user_id).first()
    if user.FoodIndex == 0:
        return TextSendMessage (text = "您已經登記過了喔！")
    if result == 0:
        #if max_food_index == 0:  ######## 沒有其他人填過
        if max_food_index > 0:   ######### 有其他人填過且填一半
            for i in range (index_s.index (max_food_index)):
                print ("i: %d , index[i]: %d" % (i , index_s[i]))
                index_s.pop (0)
            print (index_s)
        user.FoodIndex = index_s[0]
        db.session.commit ()
    elif result == 1:
        return TextSendMessage (text = "您的教會已經登記過了喔！" )

    footer = make_footer (user.FoodIndex)
    registration_view = bubble + header + body1 + ''.join (body_s) + body2 + footer
    #print (registration_view)
        
    parsed_json = json.loads(registration_view)
    flex_message = FlexSendMessage(
        alt_text='物資登記開放',
        contents = parsed_json
    )
    return flex_message 
################## index_s 已經跑了一次了 又去抓別人填剩的 最後多跑了一圈 ###########
def check_food (event , user_id):
    food_nums = food_num.query.filter (food_num.index == 1).first()
    foods = food.query.order_by(food.index).all()
    IsFood = 0
    for product in foods:
        if product.total > 0: IsFood = 1
    if food_nums.num == 0:
        text = TextSendMessage (text = "目前尚未開放登記物資！")
    elif IsFood == 0:
        text = TextSendMessage (text = "物資已全數登記完畢！")
    else:
        text = json_flex_ch (event , user_id)
        user = users.query.filter (users.Userid == user_id).first ()
        user.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        db.session.commit ()
    line_bot_api.reply_message (event.reply_token, text)

def food_booking (event , user_id , user_IsFoodBank):
    if user_IsFoodBank == 1:
        check_food (event , user_id)
    elif user_IsFoodBank == 2:
        book_food (event , user_id)
    elif user_IsFoodBank == 3:
        fix_record1 (event , user_id)
    elif user_IsFoodBank == 4:
        fix_record2 (event , user_id)
