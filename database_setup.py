from sqlalchemy import Column, ForeignKey, Integer, String, create_engine,Date
from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()
engine=create_engine('sqlite:///userdb.db')
Base.metadata.create_all(engine)

class Userdb(Base):
    __tablename__='userdata'
    sno=Column(Integer,nullable=False,autoincrement=True)
    rno = Column(Integer, nullable=False,primary_key=True)
    name=Column(String(30),nullable=False)
    sex=Column(String(7))
    age=Column(Integer)
    year=Column(Integer)
    branch=Column(String(40))
    DOB=Column(String(20))
    DOJ=Column(String(20))
    email = Column(String(20), nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    aboutu=Column(String(250))
    prflpic=Column(String(250))


Base=declarative_base()
engine=create_engine('sqlite:///friendsdb.db')
Base.metadata.create_all(engine)


class Frienddb(Base):
    __tablename__='friendsdb'
    sno=Column(Integer,nullable=False,autoincrement=True,primary_key=True)
    frsend=Column(Integer,nullable=False)
    frget=Column(Integer,nullable=False)
    sendd=Column(String(20))
    acceptd=Column(String(20))
    accept=Column(Integer)


Base=declarative_base()
engine=create_engine('sqlite:///messagesdb.db')
Base.metadata.create_all(engine)


class Messagedb(Base):
    __tablename__='messagesdb'
    sno=Column(Integer,nullable=False,autoincrement=True,primary_key=True)
    mid=Column(String(50))
    msend=Column(Integer,nullable=False)
    mget=Column(Integer,nullable=False)
    sendm=Column(String(250))
    sendd=Column(String(30))
    seend=Column(String(30))
    getv=Column(Integer)




