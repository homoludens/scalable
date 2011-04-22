# Greenlets + Gevent
import gevent
import gevent.socket as socket

def handle(sock):
    buf = sock.recv(100)
    # cpu intensive calculation
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
    t = gevent.Greenlet(handle, sock)
    t.start()

# TODO/FIXME: join all greenlets

'''

 I/O even loop:
 data event  -> handler
                  -> put cpu intensive work=(command, data) to QUEUE ->
                  -> wait for event (returns to I/O loop)
                  -> get result from thread poll

 thread poll (4 worker threads) high prio:
   read queue for work,
   do work
   signal event with result

 thread poll (10 workers) low prio
'''
