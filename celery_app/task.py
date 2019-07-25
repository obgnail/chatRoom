from celery_app import app

# from settings import DATABASE
from db import session,User,Message
from sqlalchemy import or_

# 保存信息
@app.task
def add_message(from_user,to_user,content):
    f_user = session.query(User.name).filter_by(name=from_user).first()[0]
    t_user = session.query(User.name).filter_by(name=to_user).first()[0]

    if f_user and t_user:
        new_message = Message(from_user=f_user,to_user=t_user,content=content)

        session.add(new_message)
        session.commit()
        print('************ insert successful ************')
        return True


@app.task
def add_user(name,password):
    print('************ insert start ************')
    user = User(name=name,password=password)

    session.add(user)
    session.commit()
    print('************ insert successful ************')
    return True

@app.task
def filter_sb_to_all_message(from_user):
    return session.query(Message).filter_by(from_user=from_user,to_user='all').all()


@app.task
def filter_sb_to_sb_message(from_user,to_user):
    return session.query(Message).filter_by(from_user=from_user,to_user=to_user).all()


@app.task
def filter_sb_message(from_user,to_user):
    return session.query(Message).filter(or_(Message.from_user==from_user,Message.to_user==to_user)).order_by(Message.createtime).all()


@app.task
def filter_all_to_all_message(to_user):
    return session.query(Message).filter_by(to_user='all').all()


