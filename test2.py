from db import session,User,Message


# def filter_to_all_message(from_user):
#     return session.query(Message).filter_by(from_user=f_user,to_user='all').all()

# filter_to_all_message('liangbo')


def filter_all_to_all_message(to_user):
    return session.query(Message).filter_by(to_user='all').all()

x = filter_all_to_all_message('user1')
for each in x:
    print(each.from_user)

# ws = new WebSocket("ws://127.0.0.1:8080/chat/");
