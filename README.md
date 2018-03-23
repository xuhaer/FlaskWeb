本blog使用python编写，基于flask框架+mysql数据库，前端html5+bootstrap。
对照书目:《Flask Web开发 基于Python的Web应用开发实战》。
功能对应书本中的前十四章，有用户认证、邮件通知、发表文章、管理评论、关注用户等功能。
使用：先手动创建flasky_dev数据库，然后创建数据表： $ python manage.py shell, 然后再 db.create_all()
运行blog ： $ python manage.py runserver

requirements:

alembic==0.9.8
bleach==2.1.3
blinker==1.4
certifi==2018.1.18
chardet==3.0.4
click==6.7
coverage==4.5.1
dominate==2.3.1
Flask==0.12.2
Flask-Bootstrap==3.3.7.1
Flask-HTTPAuth==3.2.3
Flask-Login==0.4.1
Flask-Mail==0.9.1
Flask-Migrate==2.1.1
Flask-Moment==0.6.0
Flask-PageDown==0.2.2
Flask-Script==2.0.6
Flask-SQLAlchemy==2.3.2
Flask-WTF==0.14.2
ForgeryPy==0.1
html5lib==1.0.1
httpie==0.9.9
idna==2.6
itsdangerous==0.24
Jinja2==2.10
Mako==1.0.7
Markdown==2.6.11
MarkupSafe==1.0
Pygments==2.2.0
PyMySQL==0.8.0
python-dateutil==2.7.0
python-editor==1.0.3
requests==2.18.4
six==1.11.0
SQLAlchemy==1.2.5
text-unidecode==1.2
urllib3==1.22
visitor==0.1.3
webencodings==0.5.1
Werkzeug==0.14.1
WTForms==2.1