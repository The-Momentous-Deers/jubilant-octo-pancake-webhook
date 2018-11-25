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
    id = Column(String, primary_key=True)
    name = Column(String)
    username = Column(String)
    password = Column(String)
    ledger_id = Column(String)

    def __repr__(self):
        return "<User(name='%s', username='%s', password='%s')>" % (
    self.name, self.username, self.password)


def addUser(session, enduser_id, enduser_name, enduser_username, enduser_password, enduser_ledger_id):
        toAdd = session.add(User(id= enduser_id, name= enduser_name, username= enduser_username, password=enduser_password, ledger_id = enduser_ledger_id))
        session.commit()

def validatePassword(session, nameEntered, passEntered):
    for name, password, id in session.query(User.name, User.password):
        if name == nameEntered and password == passEntered:
            return enduser_id
        
    return None

def updateLedgerID(session, enduser_id, make_ledger_id):
    toUpdate = session.query(User).filter_by(id = enduser_id).first()
    toUpdate.ledger_id = make_ledger_id
    session.commit()

