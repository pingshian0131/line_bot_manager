from line_bot_api import *

def stu_event (event):
    buttons_template = TemplateSendMessage(
        alt_text='助學金申請說明',
        template=ButtonsTemplate(
            title='助學金申請說明',
            text='每年寒暑假辦理說明會，申請人“必須”出席，須完成服務時數。\n對象：認養童或認養童兄姐。',
            thumbnail_image_url='https://lh3.googleusercontent.com/owxthkP1M0DxXQDtozsVy9aeHHasfGEsvl-cB33BDovDy7L_8kglMLlvyVJgHbHb_AxKTZW-Apc-GP8n19-UHfUbxw7wMtkADjWUAsCtFSRag8KlJ6q5n5d4CPwoZJ2HdPXJZTfE-exPSohqi3xqLFptHInv_5D0Tn8cHveLUvkAcZfT7KF08M1Aa7l6dmVQuiKDK5J2EklBSycEj1yDPK2ea2bPmZ9C8oIXxiKMqmDpKnoPJuTf4Rj0_Gdqt1Mwb7m95V0bbTAsG0jAqEcfVNRhotUjX1Wfbj-oySpsvGqoI9zaiZLjgfxt5pZd04mWGx40m-5npEjjgFANgD6R52gVxJjkKJ4dKkvPpDA4zPFpjDHpxD-FvffMcrUvKrcmotD6gGIZFu5PaEv5KtV2vb2iCn1kxSH1Yrp_qYlL8w8tUuMBQHqU5meBLXFl_jQCb4JnoL2dpm7FwDHkTzVFKdYnusl1EUGZlQ9jCPSIHeNu7wORxPCAym718w3gstorJlhM90BjZfX6mr20Qe79hd-5i5TPRHIab-Z6PY232Ir9n3WjSTxbgjuTAgOvrVxfVZwZ2XEKXU9bKBNGADqiKko4ChVyOJhIz-rJaSh-VHxVUGEanfEz5Zig7N-PWJ4obEEJoG3XcnPu72NaYdrVCfOgx47d4-DufrLT5j3IJTw3qpDN_fWlez9OyDsY8XLTI-6oZQktQrVn2m6bsiBwLmoyyTH8VTHp0DbhZcF3YKAtgEk=w1134-h1512-no',
            actions=[
                URITemplateAction(
                    label='助學金申請同意書202007',
                    uri='https://bit.ly/3eUaufy',
                ),
                URITemplateAction(
                    label='108-2 助學金說明會PPT',
                    uri = 'http://bit.ly/2IxPdKg',
                ),
                URITemplateAction(
                    label='109年度助學金說帖',
                    uri = 'https://bit.ly/2VGrtul',
                ),
            ]
        )   
    ) 
    line_bot_api.reply_message(event.reply_token, buttons_template)
    
