import socket

def handle(sock):
    buf = sock.recv(100)
    while buf:
        sock.send(buf)
        buf = sock.recv(100)
    sock.close()

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind(('', 9901))
sc.listen(10)

while True:
    sock, addr = sc.accept()
    print "connected from %s:%d" % addr
    handle(sock)
