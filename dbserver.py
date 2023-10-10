import logging
import socketserver
import threading

import dbserverinfo

logging.basicConfig(format="%(asctime)-15s %(message)s", filename="/var/log/dbserver/log", level=logging.DEBUG)

sema = threading.Semaphore()
waiting = 0


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global sema, waiting
        data = self.request.recv(1024)
        data = data.split()
        pid = data[0]
        operation = data[1]
        read_write = data[2]
        if operation == "acquire":
            waiting += 1
            logging.info("pid:%s %s %s %d" % (pid, operation, read_write, waiting))
            sema.acquire()
            waiting -= 1
        elif operation == "release":
            logging.info("pid:%s %s %s %d" % (pid, operation, read_write, waiting))
            sema.release()
        self.request.sendall("done")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    address = (dbserverinfo.HOST, dbserverinfo.PORT)
    server = ThreadedTCPServer(address, ThreadedTCPRequestHandler)

    server.serve_forever()
