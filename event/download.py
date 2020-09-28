from line_bot_api import *

def download_event (event):
    bubble = BubbleContainer(
        direction = 'ltr',
        hero=ImageComponent(
            url='https://lh3.googleusercontent.com/3mqWWlgURc3i8sXZsQvGmROxxApQczTRjYvmuxnqRbvsDvF_rvdfkINGt2F4gTS8NJwuKItqGZGC0wTVAGRrsRQbh-Tm8_TKj7WxnQ7yXtferCft4weB8zzPDrTFKlFw3Ix-JZbNtA=w1886-h1414-no',
            size='full',
            aspect_ratio='20:13',
            aspect_mode='cover',
        ),
        body=BoxComponent(
            layout='vertical',
            spacing='sm',
            contents=[
                # callAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='開案表', uri='https://drive.google.com/open?id=1p-0hGZ3fWazf_QffM0FvtTOQPKgrW7p6'),
                ),
                # separator
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='急難救助申請表', uri="https://drive.google.com/open?id=109f4HnfpKXde0_11tYsJGKkXBnzkku4c"),
                ),
                # separator
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='助學金申請同意書', uri="http://bit.ly/2MDnrQo"),
                ),
                # separator
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='三分量表', uri="https://donation.mustard.org.tw/MustardSurvey/Survey.aspx")
                ),
                # separator
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='申請同意書(2020年新版)', uri="https://drive.google.com/open?id=1BV3Ts9iZUTWbNqL9bos56_uEuW45s3HA"),
                ),
                # separator
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='代領切結書', uri="https://drive.google.com/open?id=1vtOrmPUtOEP13QtwdZ9l98hymj9AHLHX"),
                ),
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='專案管理人基本資料卡', uri="https://drive.google.com/file/d/1whQ7czaVZNIOBq29w9Lqgx0BR2_xGUTE/view?usp=sharing"),
                ),
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='匯款同意書', uri="https://drive.google.com/open?id=1wij4v_nv3FpZamSYUi-JJAmiRKVMnpJE"),
                ),
                SeparatorComponent(),
                # websiteAction
                ButtonComponent(
                    style='link',
                    height='sm',
                    action=URIAction(label='志願服務證明範例', uri="https://drive.google.com/file/d/1a_PVgtLB8h6IeY4-p-B8_djVsg_EEfrK/view?usp=sharing"),
                )

            ]
        )
    )
    message = FlexSendMessage (alt_text = '相關表單下載' , contents = bubble)
    line_bot_api.reply_message(event.reply_token, message)

