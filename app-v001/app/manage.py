# coding: utf-8
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# os.environ.setdefault('FLASK_ENV', 'production')
# os.environ.setdefault('FLASK_ENV', 'development')


from web import create_app, db

app = create_app(env_name='development')


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    """
    start web server
    python manage.py runserver
    """

    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    manager.run()
