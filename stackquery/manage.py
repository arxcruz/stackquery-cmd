from flask.ext.script import Manager
import apps


if __name__ == "__main__":
    app = create_app()
    manager = Manager(app)
    manager.run()
