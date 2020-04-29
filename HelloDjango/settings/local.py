from .common import *
'''
本地开发环境设置
'''

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@x_+56jnyhj^$_!u4ojj!14rh_*@+#_#^2h128btv#u&vhymd0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': os.environ.get('LOCAL_MYSQL_PASSWORD'),
        'Host': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS':
            {
                'init_command': 'SET sql_mode="STRICT_TRANS_TABLES",default_storage_engine=INNODB;',  # 设置数据库为INNODB，为第三方数据库登录用
                "unix_socket": "/tmp/mysql.sock",
            },
    }
}

