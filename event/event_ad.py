from line_bot_api import *

def event_ad (event):
    message1 = ImageSendMessage(
        original_content_url='https://i.imgur.com/LqiqBKq.jpg',
        preview_image_url='https://i.imgur.com/LqiqBKq.jpg'
    )
    text = message1
    line_bot_api.reply_message(event.reply_token , text)
