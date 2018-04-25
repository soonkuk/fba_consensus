import socket
import threading

class socket_receiver(threading.Thread):
    
    def __init__(self, socket, parent=None):
        threading.Thread.__init__(self)
        self.sock = socket
        self.parent = parent

    def received(self, thread, message):
        pass

    def run(self):
        while True:
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()
            data = self.conn.recv(65535)
            self.parent and self.parent.message_received(self, data.decode())
            # print(self.addr, data.decode())

class base_transport():
      
    def __init__(self, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        self.sock.bind(('', ip))
        self.receiver = socket_receiver(self.sock)
        self.receiver.daemon = True
        self.receiver.start()     

    def send(self, host, port, message):
        sender_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        sender_sock.connect((host, port))
        sender_sock.send(message.encode())

'''
while True:
  sock.listen(1)
  conn, addr = sock.accept()  ## conn은 접속이 체결된 소켓 객체이다.
  t = Thread(target=manage_connection, args=(conn, addr))
  t.daemon = True
  t.start()


a = base_transport(5001)
b = base_transport(5002)
while True:
    a_message = input('type message for 5001 : ')
    a.send('localhost', 5001, a_message)
    b_message = input('type message for 5002 : ')
    b.send('localhost', 5002, b_message)

'''
