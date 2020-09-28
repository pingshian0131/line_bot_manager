from line_bot_api import *
from Entity import *
from datetime import datetime
import json

index = 1
item = ""
total = 0
unit = "" 
Max = 0
fix = 0
finished = 0

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
        "color": "#5A5AAD"
      },
      {
        "type": "text",
        "text": "資",
        "weight": "regular",
        "size": "xxl",
        "align": "center",
        "color": "#5A5AAD"
      },
      {
        "type": "text",
        "text": "登",
        "weight": "regular",
        "size": "xxl",
        "align": "center",
        "color": "#5A5AAD"
      },
      {
        "type": "text",
        "text": "記",
        "weight": "regular",
        "size": "xxl",
        "align": "center",
        "color": "#5A5AAD"
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
            "text": "❗️確認此頁資料正確請按確定❗️",
            "size": "xs",
            "color": "#FF8888"
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
      },
      {
        "type": "spacer",
        "size": "lg"
      }
    ]
  },"""
footer = """
"footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "spacer",
        "size": "md"
      },
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "確定",
          "data": "data_send",
          "displayText": "物資登記已開放"
        },
        "color": "#FF0000"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "修改",
          "data": "data_fix",
          "displayText": "請輸入修改品項編號："
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "增加",
          "data": "data_add",
          "displayText": "一次增加一筆物資的資料喔😇"
        },
        "height": "sm",
        "style": "primary",
        "color": "#0000FF"
      },
      {
        "type": "spacer",
        "size": "md"
      }
    ],
    "flex": 0,
    "spacing": "xxl",
    "height": "80px",
    "borderWidth": "10px"
  },"""
styles = """
  "styles": {
    "footer": {
      "separator": true,
      "separatorColor": "#E0E0E0"
    }
  }
}"""

def reset (user_id):
    global index , item , total , unit , Max , finished 
    user = users.query.filter(users.Userid == user_id).first()
    user.State = 2
    db.session.commit()
    print ("user.State: %d" % (user.State ))
    index = 1
    item = ""
    total = 0
    unit = "" 
    Max = 0
    finished = 0

def food_postback (event , user_id):
    global fix , index , finished
    if event.postback.data == 'data_fix':
        if finished == 0:
            user = users.query.filter(users.Userid == user_id).first()
            user.State = 16
            db.session.commit()
            fix = 1
            food_nums = food_num.query.filter (food.index == 1)
            food_nums 
            text = "請輸入編號小於 " + str (food_nums) + " 。"
        else:
            text = "已經開放登記囉，無法修改！"
        return TextSendMessage(text=text)
    elif event.postback.data == 'data_send':
        if finished == 0:
            food_registrate.query.delete ()
            db.session.commit()
            reset (user_id)
            finished = 1
            fix = 0
            text = "可通知各教會開始登記物資囉！"
        else:
            text = "已經開放登記囉！"
        return TextSendMessage(text=text)
    elif event.postback.data == 'data_add':
        if finished == 0:
            user = users.query.filter(users.Userid == user_id).first()
            user.State = 12 
            food_nums = food_num.query.filter(food_num.index == 1).first()
            index = food_nums.num + 1
            food_nums.num = index
            db.session.commit()
            fix = 0
            text = "1️⃣ 請輸入品項" + str(index) + "名稱：(ex, 蘋果)"
        else:
            text = "已經開放登記囉，無法修改！"
        return TextSendMessage(text=text)

def choose_fix_item (event , user_id):
    global index , fix 
    food_nums = food_num.query.filter(food_num.index == 1).first()
    if event.message.text.isdigit ():
        if int (event.message.text) <= food_nums.num:
            index = int (event.message.text)
            user = users.query.filter(users.Userid == user_id).first()
            user.State = 17
            db.session.commit()
            text = "請輸入要修改的項目代碼:(ex , 1)\n1️⃣ 品項名稱\n2️⃣ 總數\n3️⃣ 單位\n4️⃣ 教會最大領取數量"
        else:
            text = "輸入錯誤！請輸入正確編號！"
    else:
        text = "輸入錯誤！請重新輸入阿拉伯數字！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))

def fix_food_data (event , user_id):
    global index , fix 
    if event.message.text.isdigit ():
        if int (event.message.text) <= 4 and int (event.message.text) > 0:
            if int (event.message.text) == 1:
                user = users.query.filter(users.Userid == user_id).first()
                user.State = 12
                db.session.commit()
                text = "1️⃣ 請輸入品項" + str(index) + "名稱：(ex, 蘋果)"
            elif int (event.message.text) == 2:
                user = users.query.filter(users.Userid == user_id).first()
                user.State = 13
                db.session.commit()
                text = "2️⃣ 請輸入品項" + str(index) + "數量：(ex, 300)"
            elif int (event.message.text) == 3:
                user = users.query.filter(users.Userid == user_id).first()
                user.State = 14
                db.session.commit()
                text = "3️⃣ 請輸入品項" + str(index) + "單位：(沒在下列按鈕請手動輸入)"
                unit_list = ["箱" , "盒" , "袋" , "包"]
                qr_items = []
                for unit in unit_list:
                    qr_items.append (QuickReplyButton (action = MessageAction (label = unit , text = unit)))
                quickreply = QuickReply ( items = qr_items )   
                line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text , quick_reply = quickreply))
                return 
            elif int (event.message.text) == 4:
                user = users.query.filter(users.Userid == user_id).first()
                user.State = 15
                db.session.commit()
                text = "4️⃣ 請輸入品項" + str(index) + "每間教會登記數量上限：(ex, 4)"
            line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))

        else:
            text = "輸入錯誤！請輸入正確項目代碼！"
    else:
        text = "輸入錯誤！請重新輸入阿拉伯數字！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))


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
                "text": """ + '"' + str(index) + '"' + """
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
                "text": """ + '"' + item + '"' + """
              },
              {
                "type": "text",
                "margin": "md",
                "size": "md",
                "flex": 2,
                "color": "#46A3FF",
                "align": "center",
                "contents": [],
                "text": """ + '"' + str(total) + '"'+ """
              },
              {
                "type": "text",
                "contents": [],
                "color": "#46A3FF",
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
                "text": """ + '"' + str(Max) + '"' + """
              },
              {
                "type": "text",
                "contents": [],
                "color": "#46A3FF",
                "flex": 1,
                "align": "center",
                "text": """ + '"' + unit + '"' + """,
                "size": "md"
              }
            ]
          }"""
    return body_element 

def json_flex (event):
    global bubble , header , body1 , body2 , footer , styles , separator 
    body_s = []
    food_nums = food_num.query.filter(food_num.index == 1).first()
    for i in range (1 , food_nums.num+1):
        print ("i: %d" % i)
        body_s.append (make_body_element (i))
        if i == food_nums.num: break
        body_s.append (separator)
    registration_view = bubble + header + body1 + ''.join (body_s) + body2 + footer + styles
#    print (registration_view)
    if event.message.text == '物資一覽表':
        registration_view = bubble + header + body1 + ''.join (body_s) + body2 + styles
        
    parsed_json = json.loads(registration_view)
    flex_message = FlexSendMessage(
        alt_text='物資登記開放',
        contents = parsed_json
    )
    line_bot_api.reply_message (event.reply_token, flex_message)

def close_food (event , user_id):
    global fix 
    food_nums = food_num.query.filter(food_num.index == 1).first()
    food_nums.num = 0
    reset (user_id)
    print ("food_num: %d" % food_nums.num)
    food.query.delete ()
    db.session.commit()
    if fix == 0:
        text = "物資登記已關閉"
    elif fix == 1:
        text = "資料已全數清除，請重新開始物資登記程序"
        fix = 0
    user_IsFoodBank_items = users.query.filter (users.IsFoodBank > 1).all ()
    for item in user_IsFoodBank_items:
        item.Time = None
        item.IsFoodBank = 1
        item.FoodIndex = None
        db.session.commit ()
    line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))

def set_food_data1 (event):

    alert = "❗️您已進入物資登記資料庫輸入程序，請依照問題輸入回覆、不要突然中斷或輸入其他指令，以免造成錯誤\n❗️若不得已需中斷，請直接輸入指令關閉物資登記程序。\n"
    text1 = "✳️ 請問總共有幾種品項？(最多9項)"
    text = alert + text1 
    return text 

def set_food_data2 (event , user_id):
    global index 
    if event.message.text.isdigit():
        food_nums = food_num.query.filter(food_num.index == 1).first()
        food_nums.num = int (event.message.text)
        user = users.query.filter(users.Userid == user_id).first()
        user.State = 12
        db.session.commit()
        print(event.message.text + "is insert into food_num.")
        print ("user.State: %d , food_num: %d" % (user.State , food_nums.num))
        text = "1️⃣ 請輸入品項" + str(index) + "名稱：(ex, 蘋果)"
    else:
        text = "輸入錯誤！請重新輸入阿拉伯數字！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))

def set_food_data3 (event , user_id):
    global index , item , fix 
    if fix == 0:
        item = event.message.text 
        user = users.query.filter(users.Userid == user_id).first()
        user.State = 13
        db.session.commit()
        print ("user.State: %d" % (user.State ))
        text3 = "2️⃣ 請輸入品項" + str(index) + "數量：(ex, 300)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text3))
    elif fix == 1:
        foods = food.query.filter (food.index == index).first()
        foods.item = event.message.text
        db.session.commit()
        json_flex (event)
        reset (user_id)
        fix = 0
        
def set_food_data4 (event , user_id):
    global index , total , fix 
    if event.message.text.isdigit():
        if fix == 0:
            total = int (event.message.text)
            user = users.query.filter(users.Userid == user_id).first()
            user.State = 14
            db.session.commit()
            print ("user.State: %d" % (user.State ))
            text = "3️⃣ 請輸入品項" + str(index) + "單位：(沒在下列按鈕請手動輸入)"
            unit_list = ["箱" , "盒" , "袋" , "包"]
            qr_items = []
            for unit in unit_list:
                qr_items.append (QuickReplyButton (action = MessageAction (label = unit , text = unit)))
            quickreply = QuickReply ( items = qr_items )   
            line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text , quick_reply = quickreply))

        elif fix == 1:
            foods = food.query.filter (food.index == index).first()
            foods.total = int (event.message.text)
            db.session.commit()
            json_flex (event)
            reset (user_id)
            fix = 0
    else:
        text = "輸入錯誤！請重新輸入阿拉伯數字！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))
   
def set_food_data5 (event , user_id):
    global index , unit , fix 
    if fix == 0:
        unit = event.message.text 
        user = users.query.filter(users.Userid == user_id).first()
        user.State = 15
        db.session.commit()
        print ("user.State: %d" % (user.State ))
        text5 = "4️⃣ 請輸入品項" + str(index) + "每間教會登記數量上限：(ex, 4)"
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text5))
    elif fix == 1:
        foods = food.query.filter (food.index == index).first()
        foods.unit = event.message.text 
        db.session.commit()
        json_flex (event)
        reset (user_id)
        fix = 0

def set_food_data6 (event , user_id):
    global index , item , total , unit , Max , fix  
    if event.message.text.isdigit():
        if fix == 0:
            Max = int (event.message.text)
            insert_food = food(index = index , item = item , total = total , unit = unit , Max = Max)
            db.session.add(insert_food)
            db.session.commit()
            print ("food.index: " , str (index) , " food.item: " , item , " food.total: " , str(total) , " food.unit: " , unit , " food.Max: " , str(Max))

            food_nums = food_num.query.filter(food_num.index == 1).first()
            if index == food_nums.num:
                json_flex (event)
                reset (user_id)
            else:
                index += 1
                user = users.query.filter(users.Userid == user_id).first()
                user.State = 12
                db.session.commit()
                text = "1️⃣ 請輸入品項" + str(index) + "名稱："
                line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))
        elif fix == 1:
            foods = food.query.filter (food.index == index).first()
            foods.Max = int (event.message.text)
            db.session.commit()
            json_flex (event)
            reset (user_id)
            fix = 0
    else:
        text = "輸入錯誤！請重新輸入阿拉伯數字！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))
        
def restart_food_booking (event , user_id):

    reset (user_id)
    user_id = event.message.text 
    user = users.query.filter(users.Userid == user_id).first()
    if user.IsFoodBank != None:
        user.IsFoodBank = 1
        user.FoodIndex = None
        user.Time = None 
        db.session.commit ()
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = '您已重新啟動 ' + user.Display_name + ' 物資登記功能！'))
    
def food_conversation (event , user_id , user_state):

    if user_state == 11:
        set_food_data2 (event , user_id)
    elif user_state == 12:
        set_food_data3 (event , user_id)
    elif user_state == 13:
        set_food_data4 (event , user_id)
    elif user_state == 14:
        set_food_data5 (event , user_id)
    elif user_state == 15:
        set_food_data6 (event , user_id)
    elif user_state == 16:
        choose_fix_item (event , user_id)
    elif user_state == 17:
        fix_food_data (event , user_id)
    elif user_state == 18:
        restart_food_booking (event , user_id)
