import socket
import threading

server_st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_st.bind(("", 5000))
# 创建socket,绑定端口，注意端口必须不同
password = {'a': '',
            'c': '',
            'd': ''}
# 账号密码
# 以下所有字典的键都是元组(IP,端口)
result = {}
# 服务器接收到的信息结果
login_flags = {}
# 登录状态:0/1
user = {}
# ip地址:用户名
processed = {}
# 消息处理状态:0/1


# 消息队列
def message_queuing():
    while True:
        response, address = server_st.recvfrom(1024)
        response = response.decode()
        processed[address] = 0
        # 标注该地址的这条消息未处理
        if response == '[]09-=':
            # 初始化环境
            result[address] = response
            # 该地址有一条这样的消息
            login_flags[address] = 0
            # 该地址未登录
        else:
            result[address] = response


# 消息处理函数
def message_processing():
    while True:
        work_result = result
        if work_result != {}:
            # 判断是否有用户连上服务器
            for each in list(work_result.keys()):
                # 字典result的键是连上服务器的(ip,端口)
                # 注意字典在遍历时不允许发生变化，但程序中由于多线程这是无法避免的，因此需要将此转换为列表
                # 判断登录状态，未登录标志为0
                if login_flags[each] == 0:
                    # 判断服务器接收的信息是否是初始化命令，信息是否经过处理
                    # 如果是初始化命令'[]09-='，或消息已处理的processed[each] == 1，则不执行
                    if work_result[each] != '[]09-=' and processed[each] == 0:
                        name_pw = work_result[each]
                        print('消息处理:'+name_pw)
                        name, pw = name_pw.split(':+:')
                        # noinspection PyBroadException
                        try:
                            if pw == password[name]:
                                server_st.sendto('登录成功,欢迎进入聊天室(输入聊天内容并回车发送)'.encode(), each)
                                # 登录成功，将该(ip，端口)的状态变更————消息已处理，已登录，记录元组与用户名的对应关系
                                processed[each] = 1
                                login_flags[each] = 1
                                user[each] = name
                            else:
                                server_st.sendto('用户名或密码错误,请重新输入'.encode(), each)
                                # 登录失败，只需标注消息已处理
                                processed[each] = 1
                        except BaseException:
                            server_st.sendto('不存在该用户,请重新输入'.encode(), each)
                            processed[each] = 1
                    else:
                        continue
                elif login_flags[each] == 1:
                    # 登录后，判断接收信息是否已经过处理，未处理则发送各所有为登录状态的客户机
                    if processed[each] == 0:
                        content = user[each] + ':' + work_result[each]
                        print(content)
                        for u in list(work_result.keys()):
                            # 判断登录状态
                            if login_flags[u] == 1:
                                server_st.sendto(content.encode(), u)
                        processed[each] = 1
                elif login_flags == {}:
                    continue


if __name__ == '__main__':
    threads = []
    t1 = threading.Thread(target=message_queuing)
    threads.append(t1)
    t2 = threading.Thread(target=message_processing)
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    while True:
        pass
