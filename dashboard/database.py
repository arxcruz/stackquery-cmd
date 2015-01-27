from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.jsontools import JsonSerializableBase

engine = create_engine('sqlite:///dashboard.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    
    # Creating tables
    Base.metadata.create_all(bind=engine)

    # Populating Release table
    release = models.Release()
    release.name = 'All'
    db_session.add(release)

    release = models.Release()
    release.name = 'Juno'
    db_session.add(release)

    release = models.Release()
    release.name = 'Icehouse'
    db_session.add(release)
    db_session.commit()

    # Populating User table
    user1 = models.User()
    user1.name = 'arxcruz'
    db_session.add(user1)

    user2 = models.User()
    user2.name = 'david-kranz'
    db_session.add(user2)
    db_session.commit()

    # Populating team
    team = models.Team()
    team.name = 'Demo team'
    team.users.append(user1)
    team.users.append(user2)
    db_session.add(team)
    db_session.commit()
