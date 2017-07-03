import re
import requests
import os

# r = requests.get("https://www.pgexercises.com/questions/basic/selectall.html")
# url = r.url

with open('html', 'r') as f:
    str = f.read()
print(str)

reg = re.compile(r'(\.\./.+?)"')
ziyuan = reg.findall(str)
i=0

for each in ziyuan:
    url_str = 'https://www.pgexercises.com/questions/basic/selectall.html'
    url_str=url_str[:url_str.rfind('/')]  # 先切割掉右边的内容
    while '../' in each:
        url_str = url_str[:url_str.rfind('/')]  # 每当图片的路径中有../，就切割一部分url路径
        each=each[3:]   # 然后将这一部分的../切割掉
    # pic_url = url_str+"/"+each  # 整合
    # print(pic_url)
    # pic_name = pic_url[pic_url.rfind('/')+1:]   # 取图片名

    # 下载图片并保存
    i +=1
    pic = requests.get(url_str+"/"+each)
    print(url_str+"/"+each)
    # with open(os.path.join(path, each[each.rfind('/')+1:]), 'wb') as f:
    #     f.write(pic.content)
print(i,'Done')