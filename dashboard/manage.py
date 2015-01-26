from flask.ext.script import Manager
import app

import os.path


if __name__ == "__main__":
    if not os.path.isfile('dashboard.db'):
        from database import init_db
        print "here"
        init_db()

    app = app.create_app()
    manager = Manager(app)
    manager.run()
