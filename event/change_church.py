from line_bot_api import *
from sqlalchemy import func
from datetime import datetime 
from Entity import *

tmp_user_id = ""

def change_church_event (event , user_id):
    user = users.query.filter(users.Userid == user_id).first()
    if user.State == 2:
        user.State = 8
        db.session.commit ()

#    message = "請問您要修改？\n1.專管教會"
    message = "請輸入您要修改的專管line顯示名稱："
    line_bot_api.reply_message (event.reply_token , TextSendMessage (text = message))

def input_display_name (event , user_id):

    global tmp_user_id     
    fix_target = event.message.text 
    
    user = users.query.filter(users.Userid == user_id).first()
    if user.State == 8:
        user.State = 9
        db.session.commit ()

    user_find = users.query.filter (users.Display_name == fix_target).first ()
    tmp_user_id = user_find.Userid
    print (tmp_user_id)
    if user_find == None:       
        if user.State == 8:
            user.State = 2
            db.session.commit ()
        message = "找不到" + fix_target + "，請再查詢正確的line顯示名稱。"    
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = message))
        return 
    else:
        fixing = fixed_item.query.filter (fixed_item.Display_name == fix_target).with_for_update().first ()
        currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        new_index = db.session.query(func.max(fixed_item.Id).label('max')).first ()
        if new_index.max == None:
            Id = 1
        else:
            if fixing == None:
                Id = new_index.max + 1
            else:
                fixing.update_user_id = user_id 
                fixing.update_time = currentTime 
                db.session.commit()
                line_bot_api.reply_message (event.reply_token , TextSendMessage (text = "請輸入欲修改之教會名稱："))
                return 
        insert_data = fixed_item( Id = Id , update_user_id = user_id , fixed_user_id = user_find.Userid , update_time = currentTime , Display_name = fix_target  , church_name = None)
        db.session.add(insert_data)
        db.session.commit()
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = "請輸入欲修改之教會名稱："))

def input_church (event , user_id):

    global tmp_user_id     
    user = users.query.filter(users.Userid == user_id).first()
    if user.State == 9:
        user.State = 2
        db.session.commit ()

    fixing = fixed_item.query.filter (fixed_item.update_user_id == user_id , fixed_item.fixed_user_id == tmp_user_id).first ()
    fixing.church_name = event.message.text
    db.session.commit ()
    tmp_user_id = ""

    user = users.query.filter (users.Userid == fixing.fixed_user_id).first ()
    user.Church = event.message.text
    db.session.commit ()

    message = fixing.Display_name + "的教會已修改為" + fixing.church_name 
    line_bot_api.reply_message (event.reply_token , TextSendMessage (text = message))
