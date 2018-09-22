import socket

import gevent


def client_exec(client, address):
    # 请求的数据
    request_data = client.recv(1024)
    print(request_data, address)
    if request_data:

        # 响应头
        head = "HTTP/1.1 200 ok\r\n"
        # 响应体把客户端的ip和端口再返回给客户
        body = str(address)
        # 浏览器中换行
        content = head + "\r\n" + body
        client.send(content.encode("utf-8"))
        client.close()
    else:
        client.close()
    client.close()


def main():
    """创建tcp服务器端"""
    # 初始化套接字服务器
    # 1.创建套接字
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.绑定端口与复用端口
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind(("", 8080))
    # 3.被动模式
    tcp_server.listen(128)

    # 循环去接收用户的请求
    while True:
        client, address = tcp_server.accept()
        # 处理客户端的请求
        client_exec(client, address)
        # 把任务添加到协程里面
        gevent.spawn(client_exec, client, address)

    # 关闭服务器
    tcp_server.close()


if __name__ == '__main__':
    main()
