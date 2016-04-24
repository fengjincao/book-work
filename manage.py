# -*- coding: utf-8 -*-


from bookhouse.main import create_app_main

app = create_app_main()


from flask_script import Manager


manager = Manager(app)


@manager.command
def create():
    from bookhouse.core import db

    db.create_all()


if __name__ == '__main__':
    manager.run()
