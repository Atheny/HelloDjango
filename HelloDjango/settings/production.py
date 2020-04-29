from .common import *
'''
线上环境设置，注意os.environ.get()取出环境变量，
这里用到了supervisor守护进程，目前可以在python3中安装，注意无法找到supervisord这个包的解决方法：
https://blog.csdn.net/qq_44267691/article/details/104361229
解决办法：
cd /usr/local/python3/bin（python目录），里面有echo_supervisord_conf, pidproxy, supervisorctl and supervisord 。
我们只要把supervisord复制到/usr/bin/目录下即可
cp supervisord /usr/bin/
'''

# SECURITY WARNING: keep the secret key used in production secret!
# 线上环境从环境变量获取SECRET_KEY
SECRET_KEY = os.environ.get('HELLO_DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '154.8.157.83', '.athenyblog.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': os.environ.get('ROOT_MYSQL_PASSWORD'),
        'Host': '/tmp/mysql.sock',
        'PORT': '3306',
        'OPTIONS':
            {
                'init_command': 'SET sql_mode="STRICT_TRANS_TABLES",default_storage_engine=INNODB;',  # 设置数据库为INNODB，为第三方数据库登录用
                "unix_socket": "/tmp/mysql.sock",
            },
    }
}
