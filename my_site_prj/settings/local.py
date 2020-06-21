from .base import *

DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eduocean', # 데이터베이스 이름
        'USER': 'root', # 접속 사용자 이름
        'PASSWORD': '123456789', # 접속 비밀번호
        'HOST': 'localhost',
        'PORT': '3306', # 기본 포트
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}