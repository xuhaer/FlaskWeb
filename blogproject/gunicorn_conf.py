

bind = "127.0.0.1:8000"
workers = 2
threads = 2
loglevel = 'debug'
accesslog = "./log/gunicorn_access.log"
errorlog = "./log/gunicorn_error.log"
