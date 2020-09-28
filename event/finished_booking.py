from line_bot_api import *
from Entity import *
import json

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
      },
      {
        "type": "text",
        "text": "結",
        "weight": "bold",
        "size": "xxl",
        "align": "center",
        "color": "#00AA00"
      },
      {
        "type": "text",
        "text": "果",
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
            "text": "您的教會登記的物資如下：",
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
body1_fix = """
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
            "text": "您的教會登記的物資如下：",
            "size": "md",
            "color": "#FF8888",
            "align": "center",
            "wrap": true
          },
          {
            "type": "text",
            "text": "正確請按下「送出」",
            "size": "md",
            "color": "#FF8888",
            "align": "center",
            "wrap": true
          },
          {
            "type": "text",
            "text": "‼️送出後即不能修改喔‼️ ",
            "size": "md",
            "color": "#FF8888",
            "weight": "bold",
            "align": "center",
            "wrap": true
          },
          {
            "type": "text",
            "text": "‼️請於一分鐘內確認完畢‼️ ",
            "size": "md",
            "color": "#FF8888",
            "weight": "bold",
            "align": "center",
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
  }
}"""
body2_fix = """
        ]
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
          "label": "送出",
          "data": "church_send",
          "displayText": "物資登記完成！"
        },
        "color": "#FF0000"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "修改",
          "data": "church_fix",
          "displayText": "請輸入修改品項編號："
        },
        "height": "sm",
        "style": "primary"
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
  },
  "styles": {
    "footer": {
      "separator": true,
      "separatorColor": "#E0E0E0"
    }
  }
}"""


def make_body_element1 (user_id):
    user = users.query.filter (users.Userid == user_id).first()
    
    item = []
    nums = []
    unit = []
    item_name = []
    sort = food.query.order_by(food.index).all ()
    for good in sort:
        item_name.append (good.item)

    foods = food_registrate.query.filter(food_registrate.userid == user_id).all()
    for sth in item_name:
        for aaa in foods:
            if sth == aaa.item:
                item.append (aaa.item)
                nums.append (aaa.num)
                food_item = food.query.filter (food.item == aaa.item).first ()
                unit.append (food_item.unit)
    
    body_s = []
    for index in range (len (item)):
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
                "text": """ + '"' + str(index+1) + '"' + """,
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
                "text": """ + '"' + item[index] + '"' + """,
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
                "text": """ + '"' + str(nums[index]) + '"'+ """,
                "weight": "bold"
              },
              {
                "type": "text",
                "contents": [],
                "color": "#BEBEBE",
                "flex": 1,
                "align": "center",
                "text": """ + '"' + unit[index] + '"' + """
              }
            ]
          }"""
        body_s.append (body_element)
        body_s.append (separator)
    body_s.pop ()
    return body_s 

def js_flex_fix (event , user_id):
    global bubble , header , body1_fix , body2_fix , separator , footer 
    body_s = []
    body_s = make_body_element1 (user_id)
    registration_view = bubble + header + body1_fix + ''.join (body_s) + body2_fix + footer 

#    print (registration_view)

    parsed_json = json.loads(registration_view)
    flex_message = FlexSendMessage(
        alt_text='確認登記結果',
        contents = parsed_json
    )
    return flex_message 

def js_flex_finished (event , user_id):
    global bubble , header , body1 , body2 , separator 
    body_s = []
    body_s = make_body_element1 (user_id)
    registration_view = bubble + header + body1 + ''.join (body_s) + body2

#    print (registration_view)

    parsed_json = json.loads(registration_view)
    flex_message = FlexSendMessage(
        alt_text='登記完成！',
        contents = parsed_json
    )
    return flex_message 

