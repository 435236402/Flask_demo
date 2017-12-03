# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand


app = Flask(__name__)

# 数据库连接的配置
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:mysql@172.16.160.128:3306/test1"
# 是否开启追踪修改,如果不配置，会有警告。因为该配置默认是耗性能的，之前默认是开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy 实例,可以当做是数据库的句柄
db = SQLAlchemy(app)

Migrate(app,db)

# 如果查询的时候数据库没有返回: sudo service mysql restart
manager = Manager(app)
# 添加数据库迁移的命令行操作
manager.add_command('db',MigrateCommand)


# 角色
class Role(db.Model):
    # 默认表名为:类名小写，可以使用　 __tablename__ 指定表名
    __tablename__ = "roles"
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    info = db.Column(db.String(64))
    # 与用户产生关联关系，代表当前这个角色下面的所有用户
    # 添加一个反向引用，就是给User添加了一个名为role的属性，可以通过这个属性直接取出对应的角色
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name


# 用户
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    info = db.Column(db.String(64))
    # 添加一个外键，角的这个表的的数据的id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %s %s %s %s>' % (self.id, self.name, self.email, self.password)






@app.route('/')
def index():
    return 'index'





if __name__ == '__main__':
    manager.run()