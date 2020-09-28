from line_bot_api import *


def email_postback_message(data):
    if data == 'stepA':

        message = TextSendMessage (
            text = "請點選第一張圖片依序向左滑動！"
        )
        message1 = ImageSendMessage(
            original_content_url='https://i.imgur.com/LrFlLKK.png',
            preview_image_url='https://i.imgur.com/LrFlLKK.png'
        )
        message2 = ImageSendMessage(
            original_content_url='https://i.imgur.com/ht09kaZ.png',
            preview_image_url='https://i.imgur.com/ht09kaZ.png'
        )
        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/G4kCszw.png',
            preview_image_url='https://i.imgur.com/G4kCszw.png'
        )
        message4 = TextSendMessage (
            text = "請按選單“步驟二”"
        )
        text = [message , message1 , message2 , message3 , message4]

    elif data == 'stepB':

        message4 = ImageSendMessage(
            original_content_url='https://i.imgur.com/DGyUBwo.png',
            preview_image_url='https://i.imgur.com/DGyUBwo.png'
        )
        message5 = ImageSendMessage(
            original_content_url='https://i.imgur.com/fKC3xiw.png',
            preview_image_url='https://i.imgur.com/fKC3xiw.png'
        )
        message6 = ImageSendMessage(
            original_content_url='https://i.imgur.com/fDD3th5.png',
            preview_image_url='https://i.imgur.com/fDD3th5.png'
        )
        message7 = ImageSendMessage(
            original_content_url='https://i.imgur.com/7tGP79h.png',
            preview_image_url='https://i.imgur.com/7tGP79h.png'
        )
        message = TextSendMessage (
            text = "感謝您的耐心閱讀～"
        )
        text = [message4 , message5 , message6 , message7 , message]
    
    return text 


def email_event(event):
        buttons_template = TemplateSendMessage(
            alt_text='感謝/歡迎信email寄送說明',
            template=ButtonsTemplate(
                title='感謝/歡迎信email寄送說明',
                text='成長年報、歡迎信及其他無法收email的認養人，請將信件寄回北區辦公室收，感謝您。請點選步驟一。',
                thumbnail_image_url='https://imgur.com/n8o9VEz.jpg',
                actions=[
                    PostbackAction(
                        label='步驟一',
                        display_text=None,
                        data = 'stepA'
                    ),
                    PostbackAction(
                        label='步驟二',
                        display_text=None,
                        data = 'stepB'
                    ),
                ]
            )   
        ) 
        line_bot_api.reply_message(event.reply_token, buttons_template)


