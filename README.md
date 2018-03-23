本blog使用python编写，基于flask框架+mysql数据库，前端html5+bootstrap。
对照书目:《Flask Web开发 基于Python的Web应用开发实战》。
功能对应书本中的前十四章，有用户认证、邮件通知、发表文章、管理评论、关注用户等功能。
使用：先手动创建flasky_dev数据库，然后创建数据表： $ python manage.py shell, 然后再 db.create_all()
运行blog ： $ python manage.py runserver

![效果图](https://github.com/xuhaer/FlaskWeb/blob/master/app/static/fig.png）
