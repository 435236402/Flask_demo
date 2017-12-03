# -*- coding:utf-8 -*-

from flask import Blueprint

app_cart = Blueprint('cart',__name__,
                     static_folder='static',
                     static_url_path='/python',
                     template_folder='templates')

from views import *