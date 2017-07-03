import os
# os模块可以直接调用操作系统提供的接口函数，实现对文件和目录和操作。
# 操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，这一点要注意一下。

print(os.name)  # 获取操作系统类型。如果是posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统。
# print(os.uname())  # 要获取详细的系统信息，可以调用uname()函数。

print(os.path.abspath('.')) # 查看当前目录的绝对路径

path = os.path.join(os.path.abspath('.'), 'testdir')  # 连接目录与文件名或目录。这里演示当前路径。
print(path)
# print(os.path.isdir(path)) # 判断是否是目录。其实是先判定存不存在，若不存在，返回false。若存在，再进行目录判断。可优化。
if not(os.path.exists(path)):  # 对该目录是否存在，进行判定。
    os.mkdir(path)  # 创建一个目录。使用os.makedirs(path)可以多层创建
else:
    print("dir is:",os.path.isdir(path)) # 我们可以在这里进行优化，先通过if判断其存在，再进行目录判断。
    os.rmdir(path)  # 删除目录。使用os.removedirs(path)可以多层删除


path = os.path.join(os.path.abspath('.'), "123.txt")
if not(os.path.exists(path)):   # 对该文件是否存在，进行判定。
    fp = open(path,'w')  # 直接用open方法创建文件
else:
    print("file is:",os.path.isfile(path))
    # print(os.path.splitext(path)) # 其他方法，分离扩展名，结果('/Users/mk/Desktop/myproject/mysite/myExample/123', '.txt')
    # print(os.path.split(path)) # 其他方法，分离路径和文件，结果('/Users/mk/Desktop/myproject/mysite/myExample', '123.txt')
    # print(os.rename("123.txt", 'test.py'))  # 其他方法，文件名重命名
    os.remove(path)  # 删除文件

# 这里顺便测试下文件读写
# try:
#     f = open('html', 'r')
#           读取文本文件用open('html', 'r')，读取二进制文件用open('html', 'rb')
#           要读取非UTF-8编码的文本文件，传入encoding参数。open('/Users/michael/gbk.txt', 'r', encoding='gbk')
#     print(f.read())
# finally:
#     if f:
#         f.close()

# 以上这么写实在太繁琐，所以，Python引入了with语句来自动帮我们调用close()方法。
with open('html', 'r') as f:
    print(f.read())

# 写文件
with open('html', 'w') as f:
    f.write('Hello, world!')