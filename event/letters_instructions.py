from line_bot_api import *

def letters_instructions(event):

    message = ImageSendMessage(
        original_content_url='https://i.imgur.com/c1awip1.png',
        preview_image_url='https://i.imgur.com/c1awip1.png'
    )

    message1 = ImageSendMessage(
        original_content_url='https://i.imgur.com/tGJrGfQ.png',
        preview_image_url='https://i.imgur.com/tGJrGfQ.png'
    )

    message2 = ImageSendMessage(
        original_content_url='https://i.imgur.com/oh8kTXt.png',
        preview_image_url='https://i.imgur.com/oh8kTXt.png'
    )
    
    text = [message , message1 , message2]
    line_bot_api.reply_message(event.reply_token , text )
