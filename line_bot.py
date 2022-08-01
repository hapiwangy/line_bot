from distutils.command.build_scripts import first_line_re
from pipes import Template
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)
# channel secret
handler = WebhookHandler("0350df02f7cc7120a090edadd29b72d5")
# channel access token
line_bot_api = LineBotApi("bw1gVD8FawAp1DWiOa5rFJAFVcpt6Z7mRl44cwqNq3adb7Fc+v4boVvqJ3NfKTfO8BpoUX2uammnXFq8tZAfO/hgtHYfJ9YAsczFZc7grqsr79U11cQ2n9vC1vJM/ZpQA9PP4xFn9H3q+Kpp8t3tdQdB04t89/1O/w1cDnyilFU=")

# 接收line訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']# 這個參數是為了要通過line的數位簽章
    body = request.get_data(as_text=True)# 這個是代表要以文字方式處理傳進來的訊息
    try:
        print(body, signature)
        handler.handle(body, signature)# 將讀進來的訊息和簽章做處理
    except InvalidSignatureError:
        abort(400)
    return("OK")

# echo回應，也就是回應你輸入的訊息
@handler.add(MessageEvent, message=TextMessage)
def echo_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

# 建立選單回應
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if isinstance(event.message, TextMessage):
        msg = event.message.text
        if msg == "sinasinasinasinasinasinasinasina":
            fig_url=f"https://www.google.com/imgres?imgurl=https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FDfkhrO1XUAEYkdw.jpg&imgrefurl=https%3A%2F%2Ftwitter.com%2Fsimon_puech%2Fstatus%2F1006873035855552512%3Flang%3Dzh-Hant&tbnid=kwgHAQqTiLQXLM&vet=12ahUKEwi6rKu73aT5AhVORvUHHa5fA-gQMygCegUIARDAAQ..i&docid=MqQlzJa0pJQkSM&w=600&h=400&q=image&ved=2ahUKEwi6rKu73aT5AhVORvUHHa5fA-gQMygCegUIARDAAQ"
            line_bot_api.reply_message(event.reply_token,
                                    ImageSendMessage(original_content_url=fig_url,
                                    preview_image_url=fig_url))
        else:
            txt="這個功能還沒好啦你他搭的"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=txt))
if __name__ == "__main__":
    app.run()