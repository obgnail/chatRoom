import hashlib

def md5(data):
    data += ('a3dcb4d229de6fde0db5686dee47145d' + str(time.time()))
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


# 密码加密
def encryption(password):
    salt = 'ppnn13moddkstFeb.1st(da&sdAA=A-AAAkj**Ha^a$sda//akj;adas@)'
    password += salt
    return hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()

print(encryption('123321'))