import datetime
from uuid import uuid4

import pymysql
import sqlalchemy
from sqlalchemy import create_engine,Boolean, Column, Integer, String, Text, ForeignKey ,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,mapper, sessionmaker

from settings import DATABASE


pymysql.install_as_MySQLdb()

connect = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}?{charset}'
print('======== mysql connect sussessful ========')
engine = create_engine(connect.format(**DATABASE),echo=DATABASE['echo'])

Base = declarative_base(engine)
session = sessionmaker(bind=engine)()



class User(Base):           
    __tablename__ = 'user'  
    id         = Column(Integer, primary_key=True , autoincrement=True, comment='用户id')
    uuid       = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()), comment='uuid')
    name       = Column(String(64),nullable=False,unique=True, comment='用户名')
    password   = Column(String(64), comment='用户密码')
    createtime = Column(DateTime, default=datetime.datetime.now(), comment='创建时间')
    is_black   = Column(Boolean, default=False, nullable=False, comment='是否黑名单用户')

    def __repr__(self):
        return '<User: {}>'.format(self.name)


class Message(Base):
    __tablename__ = 'message'  
    id         = Column(Integer, primary_key=True, autoincrement=True, comment='信息id')
    content    = Column(Text, comment='信息内容')
    createtime = Column(DateTime, default=datetime.datetime.now(), comment='创建时间')
    from_user  = Column(String(64),ForeignKey('user.name',ondelete='CASCADE'),nullable=False, comment='发送人')
    to_user    = Column(String(64),ForeignKey('user.name',ondelete='CASCADE'),nullable=False, comment='接收人')

    f_user = relationship("User",foreign_keys=[from_user])
    t_user = relationship("User",foreign_keys=[to_user])    

    def __repr__(self):
        return '<Message: {}>'.format(self.content)


if __name__ == '__main__':
    # user = User(uuid='464sdasdasdadsaaswe',name='heyingliang',password='8878787')
    # print(user.name)


    # m = Message(from_user='heyingliang',to_user='liangbo',content='this is content')
    # print(m)
    # session.add(m)
    # session.commit()

    # message = session.query(Message).filter_by(from_user = 'heyingliang').first()
    # print(message.from_user)
    
    # Base.metadata.create_all(engine)

    pass


