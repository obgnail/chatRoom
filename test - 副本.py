import time
import hashlib
def md5(data):
    data += ('a3dcb4d229de6fde0db5686dee47145d' + str(time.time()))
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

print(md5('何应良'))