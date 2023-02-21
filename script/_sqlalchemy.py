from sqlalchemy.orm import Session
from sqlalchemy import  insert, or_, func
from sqlalchemy import Boolean, Column, Integer, String, DateTime, LargeBinary
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/data.db"

# creating engine
# By default, check_same_thread is True and only the creating thread may use the connection. If set False,
# the returned connection may be shared across multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# bind – An optional Connectable, will be assigned the bind attribute on the MetaData instance.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A simple constructor that allows initialization from kwargs.
Base = declarative_base()


import threading
class Database:
    lock = threading.Lock()
    def __init__(self):

        self.db = SessionLocal()

    def __enter__(self):
        Database.lock.acquire()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        Database.lock.release()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

class Result:
    def __init__(self, success=True, msg="Success", data="", exception=""):
        self.success = success
        self.msg = msg
        self.data = data
        self.exception = None
        if exception:
            self.exception = exception
    def to_dict(self):
        dic = dict()
        dic["success"] = self.success
        dic["msg"] = self.msg
        dic["data"] = self.data
        if self.exception:
            dic["exception"] = self.exception
        return dic
# mailTable = Table('mail', metadata,
#                    Column('id', Integer, primary_key=True),
#                    Column('email', String),
#                    Column('password', String),
#                    # thêm các cột khác ở đây
#                    extend_existing=True, # chỉ định định nghĩa lại bảng
#                    )


class mailTable(Base):
    __tablename__ = "mail"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    password = Column(String, index=True, nullable=True)
    emailrecovery = Column(String, index=True, nullable=True)
    oldemail = Column(String, index=True, nullable=True)
    oldpassword = Column(String, index=True, nullable=True)
    oldemailrecovery = Column(String, index=True, nullable=True)
    securityquestion = Column(String, index=True, nullable=True)
    securitycode = Column(String, index=True, nullable=True)
    phonerecovery = Column(String, index=True, nullable=True)
    birthday = Column(String, index=True, nullable=True)
    groups = Column(String, index=True, nullable=True)
    user = Column(String, index=True, nullable=True)
    datecreate = Column(String, index=True, nullable=True)
    updater = Column(String, index=True, nullable=True)
    device = Column(String, index=True, nullable=True)
    youtube = Column(String, index=True, nullable=True)
    youtubepre = Column(String, index=True, nullable=True)
    country = Column(String, index=True, nullable=True)
    googleadw = Column(String, index=True, nullable=True)
    googleadsense = Column(String, index=True, nullable=True)
    chplay = Column(String, index=True, nullable=True)
    paymentmethod = Column(String, index=True, nullable=True)
    googlevoice = Column(String, index=True, nullable=True)
    language = Column(String, index=True, nullable=True)
    proxy = Column(String, index=True, nullable=True)
    proxylist = Column(String, index=True, nullable=True)
    phonehide = Column(String, index=True, nullable=True)
    datedeletephone = Column(String, index=True, nullable=True)
    logrun = Column(String, index=True, nullable=True)
    status = Column(String, index=True, nullable=True)
    status2 = Column(String, index=True, nullable=True)
    status3 = Column(String, index=True, nullable=True)
    status4 = Column(String, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.now)
    extend_existing=True



class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=True)
    user = Column(String, unique=True, index=True, nullable=True)
    password = Column(String(255), index=True, nullable=True)
    apikey = Column(String(100), index=True, nullable=True)

class Device(Base):
    __tablename__ = "device"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=True)
    user = Column(String, index=True, nullable=True)
    device = Column(String, index=True, nullable=True)
    time = Column(String, index=True, nullable=True)
    proxy = Column(String, index=True, nullable=True)
    firstmail = Column(String, index=True, nullable=True)
    namemail = Column(String, index=True, nullable=True)
    gmailchanger = Column(String, index=True, nullable=True)


from typing import Optional
# from pydantic import BaseModel

mailClass = {field.name: "" for field in mailTable.__table__.columns if field.name!="id" and field.name != "created_at" and field.name != "updated_at"}


Base.metadata.create_all(bind=engine)
