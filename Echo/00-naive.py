import socket

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind(('', 9901))
sc.listen(10)

sock, addr = sc.accept()
print "connected from %s:%d" % addr

buf = sock.recv(100)
sock.send(buf)

sock.close()
