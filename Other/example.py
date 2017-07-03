import re
import requests
import os

r = requests.get("https://www.pgexercises.com/questions/basic/selectall.html")
url = r.url

reg = re.compile(r'<img.+?src="(.+?)"')
pic_url = reg.findall(r.text)

path = os.path.join(os.path.abspath('.'), 'pic')
if not (os.path.exists(path)):  # 对该目录是否存在，进行判定。
    os.mkdir(path)  # 创建一个目录。使用os.makedirs(path)可以多层创建

for each in pic_url:
    url_str = str(url)  # url转化为字符串
    url_str=url_str[:url_str.rfind('/')]  # 先切割掉右边的内容
    while '../' in each:
        url_str = url_str[:url_str.rfind('/')]  # 每当图片的路径中有../，就切割一部分url路径
        each=each[3:]   # 然后将这一部分的../切割掉
    # pic_url = url_str+"/"+each  # 整合
    # print(pic_url)
    # pic_name = pic_url[pic_url.rfind('/')+1:]   # 取图片名

    # 下载图片并保存
    pic = requests.get(url_str+"/"+each)
    print(url_str+"/"+each)
    with open(os.path.join(path, each[each.rfind('/')+1:]), 'wb') as f:
        f.write(pic.content)
print('Done')
