#coding=utf-8
from ftplib import FTP
#设置变量
ftp = FTP()

timeout = 30  
port = 21

# 连接FTP服务器
ftp.connect('yuanxiaobo.gotoftp5.com',port,timeout)
# 登录
ftp.login('yuanxiaobo','19870616yxb')

# 获得欢迎信息
print ftp.getwelcome()

# 获取目录下的文件,获得目录列表
list = ftp.nlst()
for name in list:  
    print name

# 定义文件保存路径
name = 'abc.txt'
path = './' + name
# 打开要保存文件
f = open(path,'wb')
# 保存FTP文件
filename = 'RETR ' + name
# 保存FTP上的文件
ftp.retrbinary(filename,f.write)

# 删除FTP文件
# ftp.delete(name)

# 上传FTP文件
# ftp.storbinary('STOR test.txt', open(path, 'rb'))
# ftp.quit()