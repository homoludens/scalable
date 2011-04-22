import socket
import select

State = {}
Number = 0

def handle_in(poll, fd):
    sock, out = State[fd]
    buf = sock.recv(4096)
#    sock.send(buf)
    State[fd] = (sock, out + buf)
    poll.modify(fd, select.POLLIN | select.POLLHUP | select.POLLOUT)

def handle_out(poll, fd):
    sock, out = State[fd]
    n = sock.send(out)
    rest = len(out) - n
    if rest > 0:
        State[fd] = (sock, out[rest:])
    else:
        State[fd] = (sock, '')
        poll.modify(fd, select.POLLIN | select.POLLHUP)

def handle_other(poll, fd):
    sock, out = State[fd]
    sock.close()
    poll.unregister(fd)
    del State[fd]

def handle_acceptor(poll, sock):
    global Number
    conn, addr = sock.accept()
    Number+=1
    print "Connection %d" % Number, "from %s:%d" % addr
    fd = conn.fileno()
    State[fd] = (conn, '')
    poll.register(fd, select.POLLIN | select.POLLHUP)

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind(('', 9901))
sc.listen(socket.SOMAXCONN)
sc.setblocking(False)

poll = select.poll()
acceptor = sc.fileno()
poll.register(acceptor, select.POLLIN)

while True:
    for fd, event in poll.poll():
        if event == select.POLLIN and fd == acceptor:
            handle_acceptor(poll, sc)
        elif event == select.POLLIN:
            handle_in(poll, fd)
        elif event == select.POLLOUT:
            handle_out(poll, fd)
        else:
            handle_other(poll, fd)
