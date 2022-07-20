from email.mime.message import MIMEMessage
from re import T
from flask import Flask, request, abort
import re

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
import pymysql

#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
#             static_folder='static',
#             static_url_path='/static'
#             )
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'img')
# Channel Access Token
line_bot_api = LineBotApi('hV6rJk18a+UB/B4DNMOEzNQaq5izOR7lZ85iZG+m/WVO5cMBB/Dhji6tgZD7aR86R+7iCeuFWlnsucJkIRnmOS/XaQQB/oyqpuni0maKPGtmqMDgzx3qb+JnzAKLx6cJ3eiuSpX9xFYrHKHNFSX6dAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b723f5d1111ac7054eadeed74a284218')

db_host='sgpdb.itlab.tw'
db_user='shane'
db_password='GKbCoMubLMQ6o'
db_name='shane'
db_port=8889

user_id = 'Ud3abee7fc3caa2649e1d1573985470b1'

class DB:
    def connect(self):
        self.conn = pymysql.connect(
                             host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             port=db_port)

    def query(self, sql):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except pymysql.OperationalError:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            print('重新連線')
        return cursor
    def close(self):
        self.connect()
        self.conn.close()
db = DB()

# line_bot_api.push_message(user_id, TextSendMessage(text='你可以開始了'))
# line_bot_api.set_webhook_endpoint(<webhook_endpoint_URL>)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####

# 回覆訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('兄弟', message):
        # sql = "select m.name, m.ig_url from cpbl_member m left join cpbl_team t on m.team_id = t.id where m.team_id=1;"
        # result = db.query(sql).fetchall() # result = list
        # content = result[0]
        content = []
        sql = "select m.name, m.ig_url from cpbl_member m left join cpbl_team t on m.team_id = t.id where m.team_id = 1;"
        result = db.query(sql).fetchall() # result = list, result[0] = dict
        for m in result:
            name = m['name']
            ig = m['ig_url']
            c = name + ': ' + ig
            content.append(c)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(str('\n'.join(content))))
    # 回傳圖片
    elif re.match('貴貴', message):
        image_message = ImageSendMessage(
            original_content_url = 'https://instagram.ftpe7-1.fna.fbcdn.net/v/t51.2885-15/292996591_409357517812486_5900904124539857918_n.jpg?stp=dst-jpg_e35_s1080x1080&_nc_ht=instagram.ftpe7-1.fna.fbcdn.net&_nc_cat=110&_nc_ohc=gUROhAV3PUQAX_MdgKF&edm=ALQROFkBAAAA&ccb=7-5&ig_cache_key=Mjg3OTcxMTE2NDYwODk0MTcxNA%3D%3D.2-ccb7-5&oh=00_AT9itWV9Bg17p__aVMSnMOckWYjD8EM6TB9DigoEAepFpQ&oe=62DECB85&_nc_sid=30a2ef',
            preview_image_url = 'https://instagram.ftpe7-1.fna.fbcdn.net/v/t51.2885-15/292996591_409357517812486_5900904124539857918_n.jpg?stp=dst-jpg_e35_s240x240&_nc_ht=instagram.ftpe7-1.fna.fbcdn.net&_nc_cat=110&_nc_ohc=gUROhAV3PUQAX_MdgKF&edm=ALQROFkBAAAA&ccb=7-5&ig_cache_key=Mjg3OTcxMTE2NDYwODk0MTcxNA%3D%3D.2-ccb7-5&oh=00_AT9LtM3Sbt2eUrddtMzxrFlRkl0vXJAWgS4Lbh6GqpLphQ&oe=62DECB85&_nc_sid=30a2ef'
        )
        line_bot_api.reply_message(
            event.reply_token,
            image_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(message))
        # line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))

# 處理訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg = event.message.text
#     if '最新合作廠商' in msg:
#         message = imagemap_message()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '最新活動訊息' in msg:
#         message = buttons_message()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '註冊會員' in msg:
#         message = Confirm_Template()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '旋轉木馬' in msg:
#         message = Carousel_Template()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '圖片畫廊' in msg:
#         message = test()
#         line_bot_api.reply_message(event.reply_token, message)
#     elif '功能列表' in msg:
#         message = function_list()
#         line_bot_api.reply_message(event.reply_token, message)
#     else:
#         message = TextSendMessage(text=msg)
#         line_bot_api.reply_message(event.reply_token, message)

# @handler.add(PostbackEvent)
# def handle_message(event):
#     print(event.postback.data)


# @handler.add(MemberJoinedEvent)
# def welcome(event):
#     uid = event.joined.members[0].user_id
#     gid = event.source.group_id
#     profile = line_bot_api.get_group_member_profile(gid, uid)
#     name = profile.display_name
#     message = TextSendMessage(text=f'{name}歡迎加入')
#     line_bot_api.reply_message(event.reply_token, message)
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
