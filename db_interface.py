from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///users.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    # We will use the enduser_id as a primary key
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', username='%s', password='%s')>" % (
    self.name, self.fullname, self.password)



def addUser(session, enduser_id, enduser_name, enduser_username, enduser_password):
        toAdd = session.add(User(id= enduser_id, name= enduser_name, username= enduser_username, password=enduser_password))
        session.commit()


addUser(session)
