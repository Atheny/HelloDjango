from fabric import Connection
from invoke import Responder
import environ
'''
实际部署：
在本地环境运行：
pipenv run python fabfile.py
'''
# initialize env
env = environ.Env()

# reading .env file
environ.Env.read_env()

def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(env('github_username'))
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(env('github_username')),
        response='{}\n'.format(env('github_password'))
    )
    return [username_responder, password_responder]


def deploy():
    c = Connection(env('fab_host'), user=env('fab_user'), port=env('fab_port'), connect_kwargs={'password': env('fab_password')})

    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'HelloDjango'

    project_root_path = '~/apps/HelloDjango/'

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = 'supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装依赖
    with c.cd(project_root_path):
        c.run('pipenv install --deploy --ignore-pipfile')

    # 迁移数据库
    with c.cd(project_root_path):
        c.run('pipenv run python manage.py makemigrations')

    # 迁移数据库
    with c.cd(project_root_path):
        c.run('pipenv run python manage.py migrate')

    # 收集静态文件
    with c.cd(project_root_path):
        c.run('pipenv run python manage.py collectstatic --noinput')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = 'supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)


if __name__ == '__main__':
    deploy()