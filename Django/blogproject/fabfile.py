import os
import getpass

from fabric import Connection
from invoke import task

sudo_pass = getpass.getpass()
GIT_REPO = "https://github.com/xuhaer/Django_Blog"
con = Connection('har@120.79.135.89:22')

@task
def deploy(con):
    source_folder = '~/sites/blog.xuhaer.com/Django_Blog/'
    # con.run('cd {} && git pull'.format(source_folder), pty=True)
    con.run("""
        cd {} &&
        source /home/har/sites/blog.xuhaer.com/venv/bin/activate &&
        pip install -r requirements.txt &&
        python manage.py migrate &&
        gunicorn blogproject.wsgi:application -c ./blogproject/gunicorn_conf.py
        """.format(source_folder), pty=True)
