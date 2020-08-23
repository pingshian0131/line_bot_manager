from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from main import app
from models import Todo, ptt_articles
from views.ptt_apis import bp as ptt_api


app.register_blueprint(ptt_api, url_prefix="/ptt_api")
# 設定你的 app
manager = Manager(app)
# 設定 python manage.py db 來管理 models
manager.add_command('db', MigrateCommand)
# 設定 python manage.py runserver 為啟動 server 指令
manager.add_command('runserver', Server())


if __name__ == '__main__':
    manager.run()
