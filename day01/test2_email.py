# -*- coding:utf-8 -*-

from flask import Flask
from flask_mail import Mail,Message
from threading import Thread

app = Flask(__name__)

# 配置邮件: 服务器/端口/安全套接字层/邮箱名/授权码/ 默认发送人
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "zhouzhiliang1996@163.com"
app.config['MAIL_PASSWORD'] = "zhou123"
app.config['MAIL_DEFAULT_SENDER'] = 'FlaskAdmin<zhouzhiliang1996@163.com>'

# 初始化邮件对象,一会去发送邮件
mail = Mail(app)


def asyc_send_mail(message):
    with app.app_context():
        mail.send(message)


@app.route('/')
def index():
    return '<a href="/send_mail">发送邮件<a/>'


@app.route('/send_mail')
def send_mail():
    message = Message(subject='邮件主题',recipients=['zhouzhiliang1996@163.com'])
    message.html = '<h1>哈哈哈哈或<h1/>'
    thread = Thread(target=asyc_send_mail,args=(message,))
    thread.start()
    return '发送中...'

if __name__ == '__main__':
    app.run(debug=True)