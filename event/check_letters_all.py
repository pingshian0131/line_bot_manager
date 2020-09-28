from line_bot_api import *
from Entity import *
from datetime import datetime
from event.change_church import *

n = 0   #### 總資料數
result_list = []    ##### 每次處理的data
tmp_list = []   ##### 暫存data 丟進result_list
church = ""
extra_mode = 0   ##### 是否為carousel 是為1 , 不是為0
bubble_num = 0   ##### 正在處理的bubble頁數
num = 0   ###### bubble 總數
message_num = 0    ####### message 總數
tmp_message_num = 1    ###### 正在處理的message

def aaa():
    
    content = []
    title = TextComponent (text = church , weight = 'bold' , size = 'xl' , align = 'center' , wrap = True , color = '#0B0047')
    cp = BoxComponent ( layout = 'vertical', contents = [ title ])
    return cp

def make_bubble_data ():

    global n , result_list , extra_mode , bubble_num , tmp_list , message_num  
#    if n > 7:
    if message_num == 1 or message_num == 0:
        bubble_num = bubble_num +1
#       print (bubble_num)
        result_list = []
        ############ 主要製作每頁bubble呈現資料的位置 ##########
        if bubble_num == num:    ###### 最後一頁bubble資料製作
            for i in range ((bubble_num-1) * 7 , n , 1):
    #           print (tmp_list[i])
                result_list.append ( tmp_list[i] )
        else:   ##### 過程中每頁bubble資料製作
            for i in range ((bubble_num-1) * 7 , bubble_num * 7 , 1):
    #           print (tmp_list[i])
                result_list.append ( tmp_list[i] )
            #print (result_list[16])
    else:  ###### message_num == 2 or 3
        if tmp_message_num == 1:
            bubble_num = bubble_num +1
            result_list = []
            if bubble_num == 7:    ###### 最後一頁bubble資料製作
                for i in range ((bubble_num - 1) * 7 , 49 , 1):
        #           print (tmp_list[i])
                    result_list.append ( tmp_list[i] )
            else:   ##### 過程中每頁bubble資料製作
                for i in range ((bubble_num - 1) * 7 , bubble_num * 7 , 1):
        #           print (tmp_list[i])
                    result_list.append ( tmp_list[i] )
        elif tmp_message_num == 2 and message_num == 2:
            bubble_num = bubble_num +1
            result_list = []
            if bubble_num == (num-7):    ###### 最後一頁bubble資料製作
                for i in range ( 49 + (bubble_num - 1) * 7 , n , 1):
        #           print (tmp_list[i])
                    result_list.append ( tmp_list[i] )
            else:   ##### 過程中每頁bubble資料製作
                for i in range ( 49 + (bubble_num - 1) * 7 , 49 + bubble_num * 7 , 1):
                    print ("i: " + str(i) + " ,bubble_num: " + str (bubble_num))
                    result_list.append ( tmp_list[i] )
        elif tmp_message_num == 2 and message_num == 3:
            bubble_num = bubble_num +1
            result_list = []
            if bubble_num == (num-7):    ###### 最後一頁bubble資料製作
                for i in range ( 49 + (bubble_num - 1) * 7 , 98 , 1):
        #           print (tmp_list[i])
                    result_list.append ( tmp_list[i] )
            else:   ##### 過程中每頁bubble資料製作
                for i in range ( 49 + (bubble_num - 1) * 7 , 49 + bubble_num * 7 , 1):
        #           print (tmp_list[i])
                    result_list.append ( tmp_list[i] )
        elif tmp_message_num == 3 and message_num == 3:
            bubble_num = bubble_num +1
            result_list = []
            if bubble_num == (num-7):    ###### 最後一頁bubble資料製作
                for i in range ( 98 + (bubble_num - 1) * 7 , n , 1):
        #           print (tmp_list[i])
                    result_list.append ( tmp_list[i] )
            else:   ##### 過程中每頁bubble資料製作
                for i in range ( 98 + (bubble_num - 1) * 7 , 98 + bubble_num * 7 , 1):
        #           print (tmp_list[i])
                    result_list.append ( tmp_list[i] )

def data_count ():

    global n , result_list , extra_mode , bubble_num , tmp_list , message_num  

############### start create a flex message ###################
############### or if flex message is not carousel ############
    if extra_mode != 1:
        data_lettersData = letter_list.query.all()
        result_dict = {}
        for data in data_lettersData:
            #print (church)
            if data.church == church:
                result_dict['name'] = data.name
                result_dict['event'] = data.event
                result_dict['persons'] = data.persons
                result_dict['title'] = data.title
                if data.title == None: result_dict['title'] = '君'
                due_date = data.due.strftime("%y-%m-%d")
                result_dict['due'] = due_date
                if data.event_detail == None: result_dict['event_detail'] = 'None'
                else: result_dict['event_detail'] = data.event_detail
#                print ('!=+' , result_dict['event_detail'])
                result_list.append(result_dict)
                n = n+1
                result_dict = {}
        tmp_list = result_list.copy()
#        print ("n:" + str (n) + " , extra_mode:" + str (extra_mode) )
#        print (n)
#        print (tmp_list)
################# if flex message is carousel ##################
    else:
        if tmp_message_num == 1:
            make_bubble_data ()
        else:    ##### tmp_message_num = 2 or 3 ####
            make_bubble_data ()

def data_processing ():

    global n
    global result_list
    
    name_list = []
    event_list = []
    title_list = []
    persons_list = []

    for i in range (len(result_list)):
        name_list.append( TextComponent (text = result_list[i]['name'] , wrap = True , color = '#000000' , size = 'sm' , flex = 2 ))
        event_list.append( TextComponent (text = result_list[i]['event'] , wrap = True , color = '#000000' , size = 'sm' , flex = 2 ))
        persons_list.append( TextComponent (text = result_list[i]['persons'] , wrap = True , color = '#000000' , size = 'sm' , flex = 2 ))
        title_list.append ( TextComponent (text = result_list[i]['title'] , wrap = True , color = '#000000' , size = 'sm' , flex = 1 ))
#        print (name_list , event_list , persons_list , title_list)

    middle_list = [[] * 4 for i in range (len(result_list))]
    for i in range (len(result_list)):
        middle_list[i].append ( name_list[i] )
        middle_list[i].append ( event_list[i] )
        middle_list[i].append ( persons_list[i] )
        middle_list[i].append ( title_list[i] )
#        print (middle_list[i]) 
    return middle_list

def data_processing2 ():

    global n
    global result_list

    item = '截止日期'
    item2 = '說明'
    due_list = []
    event_detail_list = []

    for i in range (len(result_list)):
        due_list.append ( TextComponent (text = result_list[i]['due'] , wrap = True , color = '#666666' , size = 'xs' , flex = 3))
        event_detail_list.append ( TextComponent (text = result_list[i]['event_detail'] , wrap = True , color = '#666666' , size = 'xs' , flex = 3 , align = 'end' ))
    
    item_dict = TextComponent (text = item , wrap = True , color = '#666666' , size = 'sm' , flex = 3 )
    item2_dict = TextComponent (text = item2 , wrap = True , color = '#666666' , size = 'sm' , flex = 2 , margin = 'xl')
    
    middle_list = [[] * 4 for i in range (len(result_list))]
    for i in range (len(result_list)):
        middle_list[i].append ( item_dict )
        middle_list[i].append ( due_list[i] )
        middle_list[i].append ( item2_dict )
        middle_list[i].append ( event_detail_list[i] )
#        print ('***' , middle_list[i]) 
    return middle_list

def ccc():

    global n
    global result_list
    global extra_mode 

    if extra_mode == 1:
#        print ("start_data_count, tmp_message_num: " + str (tmp_message_num) )
        data_count()
    middle_list = [[] * 4 for i in range (len(result_list))]
    middle_list2 = [[] * 4 for i in range (len(result_list))]
    middle_list = data_processing ()
    middle_list2 = data_processing2 ()
    middle = []
    middle2 = []
    for i in range (len(result_list)):
        tmp = BoxComponent (layout = 'baseline', spacing='sm', contents= middle_list[i])
        tmp2 = BoxComponent (layout = 'baseline', spacing='sm', contents= middle_list2[i])
        middle.append ( tmp )
        middle2.append ( tmp2 )
#        print (middle[i]) 

    line = SeparatorComponent(color = '#00BFFF')
    
    content = []
    for i in range (len(middle_list)):
        content.append (middle[i])
        content.append (middle2[i])
        if i == len (middle_list) -1:
            break
        content.append (line)
#        print (content)
    
    big = BoxComponent (layout='vertical', margin = 'lg', spacing = 'sm' , contents = content)

    a1 = TextComponent (text = '姓名' , wrap = True , color = '#74B6F7' , size = 'sm' , flex = 2  , weight = 'bold')
    a2 = TextComponent (text = '事由' , wrap = True , color = '#74B6F7' , size = 'sm' , flex = 2  , weight = 'bold')
    a3 = TextComponent (text = '認養人' , wrap = True , color = '#74B6F7' , size = 'sm' , flex = 2  , weight = 'bold')
    a4 = TextComponent (text = '稱謂' , wrap = True , color = '#74B6F7' , size = 'sm' , flex = 1 , weight = 'bold')

    front = BoxComponent (layout = 'baseline', margin= 'lg', spacing = 'sm', contents = [a1 , a2 , a3 , a4 ])

    cp = BoxComponent (layout = 'vertical',contents = [front , big])
    return cp

def ddd():
    
    global bubble_num
    cp = BoxComponent (
        layout = 'horizontal',
        contents = [ TextComponent ( text = str(bubble_num) , align = 'end' , flex = 1 , color = '#BCBCBC' , size = 'sm') ] 
    )

    return cp    

def bubble_count ():

    global n
    global church
    global num
    global message_num 
    
    num = n//7  ###### 幾頁完整的bubble 
    if n%7 != 0:  ##### 若有最後一頁 num + 1
        num += 1   

    message_num = num//7   ##### 需要幾則message 通常一則
#    print (message_num)
    if message_num > 0 :   ##### 超過一則時 有餘數則 message_num +1 
        if num%7 != 0:
            message_num += 1

def carousel ():

    global n , church , num , extra_mode , bubble_num
    extra_mode = 1

#############if num > 7 , flex message will failed.############

    bubble_list = []
    if tmp_message_num == 1 and (message_num == 0 or message_num == 1):
        for j in range (num): 
            BubbleMessage = bubble ()
            bubble_list.append (BubbleMessage)

    elif ( tmp_message_num == 1 and message_num != 1 ) or ( tmp_message_num == 2 and message_num == 3 ):
        for j in range (7):
            BubbleMessage = bubble ()
            bubble_list.append (BubbleMessage)
    
    elif ( tmp_message_num == 2 and message_num == 2 ) or ( tmp_message_num == 3 and message_num == 3 ):
        for j in range (num - 7):
            BubbleMessage = bubble ()
            bubble_list.append (BubbleMessage)

    carousel = CarouselContainer ( bubble_list )
    bubble_num = 0
    return carousel

def bubble ():
    global church

    bubble = BubbleContainer(
        direction = 'ltr',
        header = aaa(),
        body = ccc(),
        footer = ddd(),
    )
    return bubble


def check_letters (event , user_id):
    user = users.query.filter(users.Userid == user_id).first()
    if user.State == 2 and event.message.text == '信件查詢A':
        print (user.State)
        user.State = 6
        db.session.commit()
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = '請輸入教會關鍵字'))
#        elif user.State == 2 and event.message.text == '教會名稱查詢':
#            print (user.State)
#            user.State = 6
#            db.session.commit()
#            line_bot_api.reply_message (event.reply_token , TextSendMessage(text = '請輸入教會關鍵字：'))

def ask_account (event , user_id):
    user = users.query.filter(users.Userid == user_id).first()
    if user.State == 2:
#            print (user.State)
        user.State = 7
        db.session.commit()
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = '請輸入教會關鍵字'))

#def query_account (event , user_id):
#    user = users.query.filter(users.Userid == user_id).first()
#    if user.State == 5:
##            print (user.State)
#        user.State = 2
#        db.session.commit()
#
#    church = account_list.query.filter(account_list.church == event.message.text).first()
#    account = church.account
#    pwd = church.pwd
#    text = account + '\n' + pwd
#    line_bot_api.reply_message(event.reply_token, TextSendMessage (text = text))


def check_letters_usual (event , user_id):

    global n , result_list , church , bubble_num , num , message_num , tmp_message_num , tmp_list , extra_mode 

    n = 0   #### 總資料數
    result_list = []    ##### 每次處理的data
    tmp_list = []   ##### 暫存data 丟進result_list
    church = ""
    extra_mode = 0   ##### 是否為carousel 是為1 , 不是為0
    bubble_num = 0   ##### 正在處理的bubble頁數
    num = 0   ###### bubble 總數
    message_num = 0    ####### message 總數
    tmp_message_num = 1    ###### 正在處理的message

    user = users.query.filter(users.Userid == user_id).first()
    if user.Church:
        print (user.State)
        church = user.Church
        data_count ()   ##### 計算資料量(first time) #####
        bubble_count ()
        if n > 7:
            flex = carousel ()
            if message_num > 1:
                tmp_message_num += 1
                flex1 = carousel ()
                if message_num == 3:
                    tmp_message_num += 1
                    flex2 = carousel ()
        elif n == 0:
            print (event.message.text , " is Good!")
            line_bot_api.reply_message(event.reply_token, TextSendMessage (text = '您目前沒有孩子缺繳信件！'))
            return 
        else:
            bubble_num = 1
            flex = bubble () 
        message = FlexSendMessage(alt_text=event.message.text + "信件通知", contents=flex)
        if message_num > 1:
            message1 = FlexSendMessage(alt_text=event.message.text + "信件通知", contents=flex1)
            if message_num == 3:
                message2 = FlexSendMessage(alt_text=event.message.text + "信件通知", contents=flex2)
        print (user.Church , " haven't done yet!")
        line_bot_api.reply_message(event.reply_token, message )
        if message_num > 1:
            line_bot_api.push_message(user_id , message1)
            if message_num == 3:
                line_bot_api.push_message(user_id , message2)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = '您沒有權限喔！'))

    n = 0
    result_list = []
    church = ""
    bubble_num = 0
    message_num = 0    
    tmp_message_num = 1   

def push_letters (event , user_id):

    global n , result_list , church , bubble_num , num , message_num , tmp_message_num , tmp_list , extra_mode 

    user = users.query.filter(users.Userid == user_id).first()
    user.State = 2
    db.session.commit()

    n = 0   #### 總資料數
    result_list = []    ##### 每次處理的data
    tmp_list = []   ##### 暫存data 丟進result_list
    church = ""
    extra_mode = 0   ##### 是否為carousel 是為1 , 不是為0
    bubble_num = 0   ##### 正在處理的bubble頁數
    num = 0   ###### bubble 總數
    message_num = 0    ####### message 總數
    tmp_message_num = 1    ###### 正在處理的message

    handle_church = []
    tmp_state = ""
  
#    sended = [ '貴格會清水教會',
#    ]
 
##########################北區###########################
    if event.message.text == '2j3*d%m4':
        user_data = users.query.all()
        for user in user_data:
#            if user.Church != '象山靈糧福音中心':  continue 
            try:
                if user.Church != None:
                    print (user.State)
                    church = user.Church
                    data_count ()
                    bubble_count ()
                    if n > 7:
                        flex = carousel ()
                        if message_num > 1:
                            tmp_message_num += 1
                            flex1 = carousel ()
                            if message_num == 3:
                                tmp_message_num += 1
                                flex2 = carousel ()
                    elif n == 0:
                        print (user.Church , " is Good!")
#                        line_bot_api.push_message( user.Userid , TextSendMessage (text = '您目前沒有孩子缺繳信件！'))
                        continue
                    else: #####n = 1
                        bubble_num = 1
                        flex = bubble () 
    
                    if n > 0:
                        message = FlexSendMessage(alt_text=church + "信件通知", contents=flex)
                        if message_num > 1:
                            message1 = FlexSendMessage(alt_text=church + "信件通知", contents=flex1)
                            if message_num == 3:
                                message2 = FlexSendMessage(alt_text= church + "信件通知", contents=flex2)
                        
                        tmp_state = user.Church + " haven't done yet!"
                        print (tmp_state)
    
                        line_bot_api.push_message( user.Userid , message )
                        print (user.Church , " is pushed.")
                        handle_church.append (church + '\n')
                        if message_num > 1:
                            line_bot_api.push_message( user.Userid , message )
                            print (user.Church , " is pushed.")
                            if message_num == 3:
                                line_bot_api.push_message( user.Userid , message )
                                print (user.Church , " is pushed.")
                    else:
                        tmp_state = user.Church + " haven't been sent."
                        print (tmp_state)
                        handle_church.append (church + 'no\n')
            except:
                print (user.Church + " is ERROR!!!!!")    

            n = 0   #### 總資料數
            result_list = []    ##### 每次處理的data
            tmp_list = []   ##### 暫存data 丟進result_list
            church = ""
            extra_mode = 0   ##### 是否為carousel 是為1 , 不是為0
            bubble_num = 0   ##### 正在處理的bubble頁數
            num = 0   ###### bubble 總數
            message_num = 0    ####### message 總數
            tmp_message_num = 1    ###### 正在處理的message
       
        message = ''.join (handle_church)
        print (message)
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = message) )

def check_letters_next (event , user_id):

    global n , result_list , church , bubble_num , num , message_num , tmp_message_num , tmp_list , extra_mode 

    user = users.query.filter(users.Userid == user_id).first()
    user.State = 2
    db.session.commit()
    print (user.State)

    n = 0   #### 總資料數
    result_list = []    ##### 每次處理的data
    tmp_list = []   ##### 暫存data 丟進result_list
    church = ""
    extra_mode = 0   ##### 是否為carousel 是為1 , 不是為0
    bubble_num = 0   ##### 正在處理的bubble頁數
    num = 0   ###### bubble 總數
    message_num = 0    ####### message 總數
    tmp_message_num = 1    ###### 正在處理的message


    church = event.message.text
    data_count ()
    bubble_count ()
    print ("message_num: " + str(message_num) + " tmp_message_num: " + str (tmp_message_num) )
    if n > 7:
        flex = carousel ()
        if message_num > 1:
            tmp_message_num += 1
            print ("flex1_started")
            flex1 = carousel ()
            if message_num == 3:
                tmp_message_num += 1
                print ("flex2_started")
                flex2 = carousel ()
    elif n == 0:
        print (event.message.text , " is Good!")
        line_bot_api.reply_message(event.reply_token, TextSendMessage (text = event.message.text + '目前沒有孩子缺繳信件！'))
        return 
    else:
        bubble_num = 1
        flex = bubble ()
    message = FlexSendMessage(alt_text=event.message.text + "信件通知", contents=flex)
    if message_num > 1:
        message1 = FlexSendMessage(alt_text=event.message.text + "信件通知", contents=flex1)
        if message_num == 3:
            message2 = FlexSendMessage(alt_text=event.message.text + "信件通知", contents=flex2)

#    print (message)
    
    print (event.message.text , " haven't done yet!")
    line_bot_api.reply_message(event.reply_token, message )
    if message_num > 1:
        line_bot_api.push_message(user_id , message1)
        if message_num == 3:
            line_bot_api.push_message(user_id , message2)
    n = 0
    result_list = []
    church = ""
    bubble_num = 0
    message_num = 0    
    tmp_message_num = 1   

def church_fuzzy_query (event , user_id):

    user = users.query.filter(users.Userid == user_id).first()
    user.State = 3
    db.session.commit()
    print (user.State)

    church_list = letter_list.query.filter(letter_list.church.like ("%" + event.message.text + "%")).all()
    print (church_list)
    church_full_name = []
    if church_list:
        for item in church_list:
            if item.church not in church_full_name:
                church_full_name.append(item.church)
    else:
        text = '找不到' + event.message.text
        user = users.query.filter(users.Userid == user_id).first()
        user.State = 2
        db.session.commit()
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = text))
        return 

    church_button = []
    if len (church_full_name) < 14:
        for i in church_full_name:
            church_button.append (QuickReplyButton ( action = MessageAction ( label = i , text = i)))
        qr = QuickReply( items = church_button)
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = '請點選快捷按鈕' , quick_reply = qr))
    else:
        text = '選項太多，請輸入清楚一點的條件'
        user = users.query.filter(users.Userid == user_id).first()
        user.State = 2
        db.session.commit()
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = text))

def church_fuzzy_query2 (event , user_id):

    user = users.query.filter(users.Userid == user_id).first()
    user.State = 5
    db.session.commit()
    print (user.State)

    church_list = account_list.query.filter(account_list.church.like ("%" + event.message.text + "%")).all()
    print (church_list)
    church_full_name = []
    if church_list:
        for item in church_list:
            if item.church not in church_full_name:
                church_full_name.append(item.church)
    else:
        text = '找不到' + event.message.text
        user = users.query.filter(users.Userid == user_id).first()
        user.State = 2
        db.session.commit()
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = text))
        return
    
    church_button = []
    if len (church_full_name) < 14:
        for i in church_full_name:
            church_button.append (QuickReplyButton ( action = MessageAction ( label = i , text = i)))
        qr = QuickReply( items = church_button)
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = '請點選快捷按鈕' , quick_reply = qr))
    else:
        text = '選項太多，請輸入清楚一點的條件'
        user = users.query.filter(users.Userid == user_id).first()
        user.State = 2
        db.session.commit()
        line_bot_api.reply_message (event.reply_token , TextSendMessage (text = text))

    
def check_state (event , user_id , user_state):
    print (user_state)
    if user_state == 3:
        check_letters_next (event , user_id)
    elif user_state == 4:
        push_letters (event , user_id)
#    elif user_state == 5:
#        query_account (event , user_id)
    elif user_state == 6:
        church_fuzzy_query (event , user_id)
    elif user_state == 7:
        church_fuzzy_query2 (event , user_id)
    elif user_state == 8:
        input_display_name (event , user_id)
    elif user_state == 9:
        input_church (event , user_id)
