from line_bot_api import *

def emergency_postback(data):
    if data == 'type':
        message = TextSendMessage (
            text = """喪葬慰問金：死亡證明書。
天然災害：照片、災損證明。
重大生活事故：診斷證明、醫療費用單據、其他證明文件 ( ex, 身障證明、保護令、入監證明、......等)"""
        ) 
    elif data == 'ask':

        message = TextSendMessage (
            text = "1.申請表的申請人為孩子親屬，下方請申請人簽名，中間孩子姓名的欄位寫認養童姓名。(申請表請在下方選單中點選相關文件下載)\n2.必要文件：戶籍謄本、存摺（申請人的存摺)\n3.資料收集完後上傳系統、提出申請，社工將會與案家約家訪。"
        )
    text = message
    return text


def emergency_event(event):
        buttons_template = TemplateSendMessage(
            alt_text='急難申請說明',
            template=ButtonsTemplate(
                title='急難救助金申請說明',
                text='為因應本會認養童之家庭及安置個案家庭發生重大變故，協助其改善家庭之經濟狀況，提供急難救助金。',
                thumbnail_image_url='https://lh3.googleusercontent.com/eFksyHelL6Bh8HjEqqrfmZnG4tZb7yV1ba_uvRWcTV-qRJh-w3Fe-t1n12U39GWjvLn1F4qAVyLZnUt8ONChVLbkXcK5r4ai3_phZn3LsRWolsS1pI1ck5t-zBpNDX50ob-Jti9OhcuS2pXQ3v6VUdwt7exaCCWyU_WOD-jQTdNuOHaOxOHVkIPhySWosP-QEpSl23qDUe9vWLr8SZCa3d1wwWMsGZvJ9lwq_bIrVqT43IeoSCUYnjN9saAJeDxUpb3XdK_noW-rvbQ0AeaLzIW6P0MybJUgjMBiM10upU84gRhkrxTCrGDTCh8vqqszJ6SIs-AGMnGvXviC80W-kcrt1RYRRfgbar0wnWEvigoz1iBAhnKUEKl0M-TONtUJzexLQPq4amiNU3RCopLgOuHqm4glBo6bEyY2aIEEZA8Ihm3OBecfIHddoy-092hyRQfPvyPeDLjjipJaYhpmBPuqv9BnH8f0xQREyIiME6yLql-8sdQ3wdHYyl-iSX4lLp411lxTHNAotoewP-ltoNQ-JctukpKTZtRuU1L3JzU5e-SO4YjyG17MaFwZM-R4ZkQ68YkM8ymCaSeDb9LkaZd7aiFqXpwWLdUkBlC_y7OZ7QBSKjnCwVLXpObNrhsjUyxu_cHLnZgYA8kNPlpG-FGku_On6zwKH3xFIN8FizEvrLvuhl8HbvQq6Z4glfB6moQpUzncXSYtii81lPp5bnY2=w1124-h1498-no',
                actions=[
                    URITemplateAction(
                        label='急難救助申請表',
                        uri='https://drive.google.com/open?id=109f4HnfpKXde0_11tYsJGKkXBnzkku4c'
                    ),
                    PostbackAction(
                        label='相關說明',
                        display_text=None,
                        data = 'ask'
                    ),
                    PostbackAction(
                        label='類型',
                        display_text=None,
                        data = 'type'
                    ),
                ]
            )   
        ) 
        line_bot_api.reply_message(event.reply_token, buttons_template)


