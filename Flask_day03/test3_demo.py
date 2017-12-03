# -*- coding:utf-8 -*-\

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
# 数据库连接的配置
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:mysql@127.0.0.1:3306/test2"
# 是否开启追踪修改,如果不配置，会有警告。因为该配置默认是耗性能的，之前默认是开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "aaaaa"

db = SQLAlchemy(app)

manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)


class AddBookForm(FlaskForm):
    author_name = StringField('作者：', validators=[InputRequired()])
    book_name = StringField('书名：', validators=[InputRequired()])
    submit = SubmitField('提交')


# 作者
class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    books = db.relationship('Book', backref='author', lazy='dynamic')


# 书籍
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print e
            flash('删除失败')
            db.session.rollback()
    else:
        flash('该书不存在')
    return redirect(url_for('index'))


@app.route('/delete_author/<int:author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        try:
            # 删除书
            Book.query.filter_by(author_id=author.id).delete()
            # 删除作者
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            flash('删除失败')
    else:
        flash('该作者不存在')

    return redirect(url_for('index'))


@app.route('/', methods=['get', 'post'])
def index():
    add_book_form = AddBookForm()
    # 大写的值
    if add_book_form.validate_on_submit():
        # 取到提交的数据
        author_name = add_book_form.author_name.data
        book_name = add_book_form.book_name.data

        author = Author.query.filter_by(name=author_name).first()

        if author:
            # 如果作者存在
            book = Book.query.filter_by(name=book_name).first()
            if book:
                flash('该作者已存在同名书籍')
            else:
                # 对数据库的修改操作需要捕获异常
                try:
                    # 添加数据
                    book = Book(name=book_name, author_id=author.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    print e
                    # 回滚
                    db.session.rollback()
                    flash('数据添加失败')
        else:
            try:
                # 如果作者不存在，那么直接将作者和书直接添加到数据库
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()

                # 初始化book并添加
                book = Book(name=book_name, author_id=author.id)
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                print e
                db.session.rollback()
                flash('数据添加失败')
        print author_name, book_name
    else:
        if request.method == "POST":
            flash('输入有误')
    authors = Author.query.all()
    return render_template('temp2_demo.html', authors=authors, form=add_book_form)


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    #
    # # 生成数据
    # au1 = Author(name='老王')
    # au2 = Author(name='老尹')
    # au3 = Author(name='老刘')
    # # 把数据提交给用户会话
    # db.session.add_all([au1, au2, au3])
    # # 提交会话
    # db.session.commit()
    # bk1 = Book(name='老王回忆录', author_id=au1.id)
    # bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    # bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    # bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    # bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # # 把数据提交给用户会话
    # db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # # 提交会话
    # db.session.commit()
    #
    # app.run(debug=True)
    manager.run()
