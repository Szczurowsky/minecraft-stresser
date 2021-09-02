from .utility import pack_varint, pack_string, int_to_unsigned


class HandshakePacket:

    def __init__(self, protocol, address, port, next_state):
        self.protocol = protocol
        self.address = address
        self.port = port
        self.next_state = next_state

    def get_packet(self):
        packet = b'\x00' + pack_varint(self.protocol) + pack_string(self.address) + int_to_unsigned(self.port) + \
                 pack_varint(self.next_state)
        return pack_varint(len(packet)) + packet
