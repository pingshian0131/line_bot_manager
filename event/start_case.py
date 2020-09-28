from line_bot_api import *

def start_case_postback_message(data):
    if data == '2':

        message1 = ImageSendMessage(
            original_content_url='https://i.imgur.com/ua69Klr.jpg',
            preview_image_url='https://i.imgur.com/ua69Klr.jpg'
        )
        message2 = ImageSendMessage(
            original_content_url='https://i.imgur.com/WgdwlMk.jpg',
            preview_image_url='https://i.imgur.com/WgdwlMk.jpg'
        )
        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/qhJisCO.jpg',
            preview_image_url='https://i.imgur.com/qhJisCO.jpg'
        )
        text = [ message1 , message2 , message3 ]
    
    elif data == '3':

        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/shG64ol.jpg',
            preview_image_url='https://i.imgur.com/shG64ol.jpg'
        )
        text = message3
        
    elif data == '4':

        message4 = TextSendMessage (
            text = """1.芥菜種案家申請同意書(2020年新版)\n2.戶籍謄本（需有記事）\n3.孩子的存摺（若無需寫代領同意書）\n4.低收、弱勢兒少、特境相關政府經濟補助證明文件（若均無需附財稅資料、可至國稅局調）\n5.三分量表\n6.孩子的獨照、家中各房室照片、全家福或生活照\np.s.孩子照片可以挑可愛一點、五官清晰的，最重要的是「不能洩漏個人資訊」（像是制服、背景有月曆等）。"""
        )
        text = message4
    
    elif data == '5':
        
        message = TextSendMessage (
            text = """(若無就不用附)
1.家中成員身障證明、診斷證明、發展評估報告書
2.在監證明
3.離婚協議書、保護令"""
        )
        text = message

    elif data == '6':
        
        message = TextSendMessage (
            text = "1.孩子個資\n2.家庭成員\n3.社會資源使用狀況\n4.個案狀況說明"
        )
        text = message

    elif data == '7':

        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/9g9vAEh.jpg',
            preview_image_url='https://i.imgur.com/9g9vAEh.jpg'
        )
        text = message3

    elif data == '8':

        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/4Z7EhV7.jpg',
            preview_image_url='https://i.imgur.com/4Z7EhV7.jpg'
        )
        text = message3

    elif data == '9':

        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/Tt9mYvw.jpg',
            preview_image_url='https://i.imgur.com/Tt9mYvw.jpg'
        )
        text = message3

    elif data == '10':

        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/J16SakD.jpg',
            preview_image_url='https://i.imgur.com/J16SakD.jpg'
        )
        text = message3

    elif data == '11':

        message3 = TextSendMessage (
            text = """請參考此連結：http://bit.ly/2KqgJLz\n再加上第三點「家庭遭遇之困難」、詳述案家狀況，會對開案流程上有很大的幫助喔！"""
        )
        text = message3

    elif data == '12':

        message3 = ImageSendMessage(
            original_content_url='https://i.imgur.com/Diq1Q3P.jpg',
            preview_image_url='https://i.imgur.com/Diq1Q3P.jpg'
        )
        message4 = ImageSendMessage(
            original_content_url='https://i.imgur.com/k26EkG9.jpg',
            preview_image_url='https://i.imgur.com/k26EkG9.jpg'
        )
        text = [message3 , message4]
    
    return text

def start_case_event(event):
        carousel_template_message = TemplateSendMessage(
            alt_text='開案說明',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/vJG7ZvQ.jpg',
                        title='認養童開案',
                        text='請點選以下項目以獲得服務介紹。認養同意書、個資不公開聲明書請至“相關表單下載”中下載。',
                        actions=[
                            URIAction(
                                label='開案表範例',
                                uri = 'line://app/1600305289-EKqAy0yR'
                            ),
                            PostbackAction(
                               label='補助對象&金額',
                               display_text='協助社區中經濟困難之家庭兒童與少年就學、生活、醫療支出所需，減輕家庭撫養照顧之負擔，幫助兒童及少年順利完成學業。分為認養金及助學金',
                               data = '2'
                            ),
                            PostbackAction(
                               label='服務終止條件',
                               display_text='暫發v.s.結案',
                               data = '3'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/utR1pdb.jpg',
                        title='檢附相關文件',
                        text='因需要進行經濟審核及個資的確認，請專管協助取得各項必要文件及可附上之相關證明文件。',
                        actions=[
                            PostbackAction(
                                label='必要文件',
                                display_text=None,
                                data='4'
                            ),
                            PostbackAction(
                                label='非必要文件',
                                display_text=None,
                                data='5'
                            ),
                            PostbackAction(
                                label='必要資料',
                                display_text=None,
                                data='6'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/pvJi60f.jpg',
                        title='系統填寫說明',
                        text='基本資料頁',
                        actions=[
                            PostbackAction(
                                label='孩子個人資料頁',
                                display_text=None,
                                data='7'
                            ),
                            PostbackAction(
                                label='家庭成員',
                                display_text=None,
                                data='8'
                            ),
                            PostbackAction(
                                label='社會資源使用狀況',
                                display_text=None,
                                data='9'
                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/2GbSyk1.jpg',
                        title='個案狀況說明',
                        text='這邊的欄位關係到我們要跟認養人介紹孩子、攸關案家是否能通過，資料請「盡量填寫」。',
                        actions=[
                            PostbackAction(
                                label='系統資料頁',
                                display_text=None,
                                data='10'
                            ),
                            PostbackAction(
                                label='遭遇困難及所需協助',
                                display_text=None,
                                data='11'
                            ),
                            PostbackAction(
                                label='其他欄位',
                                display_text=None,
                                data='12'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token , carousel_template_message) 


