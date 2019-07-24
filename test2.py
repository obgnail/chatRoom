# from db import session,User,Message


# # def filter_to_all_message(from_user):
# #     return session.query(Message).filter_by(from_user=f_user,to_user='all').all()

# # filter_to_all_message('liangbo')


# def filter_all_to_all_message(to_user):
#     return session.query(Message).filter_by(to_user='all').all()

# x = filter_all_to_all_message('user1')
# for each in x:
#     print(each.from_user)

# # ws = new WebSocket("ws://127.0.0.1:8080/chat/");


from uuid import uuid4

name = '匿名用户' + str(uuid4())[:8]
print(name)


<script>
    function login_func() {
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/login/",
            data: $('#login_form').serialize(),
            success: function(res, textStatus) {
                if (textStatus == 'success' && res) {
                    if(res['status'] != 1) {
                        alert("用户已存在");
                    }
                }
                else{
                    alert("error");
                }
            }
        });
    }
</script>


async def login(request):
    data = await request.post()
    name = data['user']
    password = data['password']

    if not name:
        name = '匿名用户' + str(uuid4())[:8]
    if not password:
        password = str(uuid4())

    if not session.query(User).filter_by(name=name,password=password).first():
        task.add_user.delay(name,password)
    return aiohttp_jinja2.render_template('chatroom.html',request,{})


