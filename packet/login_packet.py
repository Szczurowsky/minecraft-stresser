from .utility import pack_varint, pack_string


class LoginPacket:

    def __init__(self, nickname):
        self.nickname = nickname

    def get_packet(self):
        packet = b'\x00' + pack_string(self.nickname)
        return pack_varint(len(packet)) + packet
