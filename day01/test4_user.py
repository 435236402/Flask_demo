# -*- coding:utf-8 -*-

from flask import Blueprint

# 创建蓝图,并指定蓝图的名字,和所在模板(用于静态和模板文件查找)
app_user = Blueprint('app_user',__name__)


# 用户信息
@app_user.route('/user_info')
def user_info():
    return 'user_info'