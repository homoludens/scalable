# threading
import socket
import threading


def handle(sock):
    buf = sock.recv(100)
    while buf:
        sock.send(buf)
        buf = sock.recv(100)
    sock.close()

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind(('', 9901))
sc.listen(socket.SOMAXCONN)


Number = 0
while True:
    sock, addr = sc.accept()
    Number+=1
    print "Connection %d" % Number, "from %s:%d" % addr
    t = threading.Thread(target=handle, args=(sock,))
    t.start()

# TODO/FIXME: join all threads
