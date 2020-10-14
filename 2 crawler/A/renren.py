# SJTU EE208

import re
import urllib.parse
import urllib.request
from http import cookiejar

from bs4 import BeautifulSoup

# 1. 构建一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()

# 2. 使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
cookie_handler = urllib.request.HTTPCookieProcessor(cookie)

# 3. 通过build_opener()来构建opener
opener = urllib.request.build_opener(cookie_handler)

# 4. addheaders接受一个列表，里面每个元素都是一个headers信息的元组，opener附带headers信息
opener.addheaders = [("User-Agent", "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110Safari/537.36")]

# 5. 需要登陆的账号和密码, 此处需要使用你们自己注册的账号密码
data = {"email": "18202101965", "password": "sjtujyx"}

# 6. 通过urlencode转码
postdata = urllib.parse.urlencode(data).encode("utf8")

# 7. 构建Request请求对象，包含需要发送的用户名和密码
request = urllib.request.Request("http://www.renren.com/PLogin.do", data=postdata)

# 8. 通过opener发送这个请求，并获取登陆后的Cookie值
opener.open(request)

# 9. opener包含用户登陆后的Cookie值，可以直接访问那些登陆后才能访问的页面
response = opener.open("http://www.renren.com/974663514/profile")
soup = BeautifulSoup(response.read())

# 下面的代码部分需要你们自己编写，主要是寻找并打印相关姓名、学校、生日和地址。
info = {}

info['name'] = soup.find('a', {'class': 'hd-name'}).string
info['school'] = soup.find('li', {'class': 'school'}).contents[0].string
temp_label = soup.find('li', {'class': 'birthday'}).contents
info['sex'] = temp_label[1].string
info['birthday'] = temp_label[3].string[1:]
info['address'] = soup.find('li', {'class': 'address'}).string

for content in info:
    print(info[content])