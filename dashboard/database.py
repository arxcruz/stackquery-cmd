from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.jsontools import JsonSerializableBase

engine = create_engine('sqlite:///dashboard.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base(cls=(JsonSerializableBase,))
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    release = models.Release()
    release.name = 'Juno'
    db_session.add(release)
    db_session.commit()

