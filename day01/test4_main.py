# -*- coding:utf-8 -*-

from flask import Flask

# 循环导入,在用的时候导入
from test4_user import app_user
from test4_order import order_list
from cart import app_cart

app = Flask(__name__)

# 直接使用调用装饰器函数的方式去注册路由
app.route('/order_list')

# 注册蓝图,将蓝图中定义好的视图和路由的映射关系注册到 app 中
app.register_blueprint(app_user,url_prefix='/user')
app.register_blueprint(app_cart,url_prefix='/cart')




@app.route('/')
def index():
    return 'index'


# # 用户信息
# @app.route('/user_info')
# def user_info():
#     return 'user_info'


# 订单信息
@app.route('/order_list')
def order_list():
    return 'order_list'


if __name__ == '__main__':
    print app.url_map
    app.run()