from line_bot_api import *

def system_event(event):
        buttons_template = TemplateSendMessage(
            alt_text='系統連結',
            template=ButtonsTemplate(
                title='系統連結',
                text='以下是常用連結，需要請點一下：',
                thumbnail_image_url='https://lh3.googleusercontent.com/MBcfdMYt6n-PR07dYGJc2N0i45xl2TaM1lGJT1J8192TlF7MyRK3PWNMTOCIYggSC1qdRhhpkjxVU6PwdUuxzGNuxzuLJ6sm0kFKoCxyOyLZgnObntzYiwmElgTk4v4ccEJYweyfvKgkr05V9rUj2YFkxMGldrOlM5Ppuw01v_YXmdS6LXPCzORu8j8fENTjyol2oYGiEEkejhkcMewjeEvQsF0Dl1Wo6BUA3njzHOV3DFyDeLGhLsU58yqHzgNaQ2byD5bd8Ju72DxfZwaNLyTQFbEDJuvU71HvZtclKTLaRLzMHGbtWK4zkf7zcp5HauJO_rj9_f_oF7wzvw374u_N51cmduLzwfQmSs7blrYfyYfPhY7-TPGWCf6veWX2rQrS9ZwhWkwVQmx5Mg7UTtEQQg7L1ve300y_jUAKkkVSGkj7MHnxsoVfsPQ08USe_IpiOl7lTDQpP-RZAMKzfbNYBMaP24Tym3YGoF4W9UFWR1tPyCX3RD3CvsW6kLT0xvDxDo6vX5Bkx8tp43q4DjTLXm-LNaR-Ed0YMj2utZyMpFPPDyBZh2AZzoYt7cicVZL9I5AH7d7hOJHVyhebp9yu0vBEUvuWir8Eyk0C22a7YwXeyvaV32lsdWIiMgHKa9zMBwxkENCRLMhJRRW1uCyiWEVHnR8ouEUJbtYz9wbRiZSkoYRFM3Mfordliu0Vd6W4ZPVpbTcfIFxnge-C9tXL=w1770-h862-no',
                actions=[
                    URITemplateAction(
                        label='訪視打卡、寄送賀卡、禮物發放',
                        uri='https://donation.mustard.org.tw/pad/'
                    ),
                    URITemplateAction(
                        label='個案管理系統',
                        uri='https://donation.mustard.org.tw/index.asp'
                    )
                ]
            )   
        ) 
        line_bot_api.reply_message(event.reply_token, buttons_template)

