import socket
import threading

client_st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_st.bind(("", 8000))
# 创建socket,绑定端口，注意端口必须不同
ip = '127.0.0.1'
# LoopBack Address 回环地址约等于 localhost 本地ip地址
address = (ip, 5000)
# 服务器ip地址与端口
flag = 0
# 登录状态标志


# 客户端主程序
def mains():
    global flag
    # 使用全局变量flag
    while True:
        # 已登录
        if flag == 1:
            content = input()
            # 输入聊天内容，以数字2作为退出命令
            # noinspection PyBroadException
            try:
                if int(content) == 2:
                    client_st.close()
                    flag = 2
                    break
            except BaseException:
                pass
            client_st.sendto(content.encode(), address)
        # 未登录
        elif flag == 0:
            print("-------------------")
            name = input('请输入用户名：')
            pw = input('请输入密码：')
            massage = name + ':+:' + pw
            # 将账号和密码通过‘:+:’拼接发送（可以尝试通过JSON发送）
            client_st.sendto(massage.encode(), address)
            res, addr = client_st.recvfrom(1024)
            res = res.decode()
            print("-------------------")
            print(res)
            # 打印结果，改变登录状态
            if '登录成功' in res:
                flag = 1


# 监听程序
def listen():
    global flag
    while True:
        # 当全局变量flag == 1 标志登录后，该监听程序才真正运行
        if flag == 1:
            response, addresses = client_st.recvfrom(1024)
            response = response.decode()
            print(response)
        elif flag == 2:
            # flag == 2 关闭该线程
            break


if __name__ == '__main__':
    print('欢迎进入聊天室')
    client_st.sendto('[]09-='.encode(), address)
    # '[]09-='作为初始化标志，当用户机连上服务器时立即发送，在服务器中，初始化该用户信息
    t = threading.Thread(target=listen)
    # 利用多线程监听服务器返回信息，注意target后的函数别加括号
    t.setDaemon(True)
    t.start()
    mains()


