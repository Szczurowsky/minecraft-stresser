import struct


def pack_string(text):
    """
    Pack a varint-prefixed utf8 string.
    """

    text = text.encode("utf-8")
    return pack_varint(len(text), max_bits=16) + text


def unpack_string(self):
    """
    Unpack a varint-prefixed utf8 string.
    """

    length = self.unpack_varint(max_bits=16)
    text = self.read(length).decode("utf-8")
    return text


def pack_varint(number, max_bits=32):
    """
    Packs a varint.
    """

    number_min = -1 << (max_bits - 1)
    number_max = +1 << (max_bits - 1)
    if not (number_min <= number < number_max):
        raise ValueError("varint does not fit in range: %d <= %d < %d"
                         % (number_min, number, number_max))

    if number < 0:
        number += 1 << 32

    out = b""
    for i in range(10):
        b = number & 0x7F
        number >>= 7
        out += struct.pack("B", b | (0x80 if number > 0 else 0))
        if number == 0:
            break
    return out


def read_port(buff):
    """ We're taking byte after server address - buff[3] (byte with length of server address) + 4 (plus quantity of
        bytes to the byte 3 - 0,1,2 plus our byte which equals 4) and one before last byte """
    port = buff[buff[3] + 4:buff[0]]
    return struct.unpack(">H", port)[0]


def read_string(buffer, position):
    length = buffer[position]
    position = position + 1
    final = bytearray()
    i = 0
    while i < length:
        final.append(buffer[position + i])
        i += 1
    return final.decode("utf-8")


def int_to_unsigned(integer):
    return struct.pack(">H", integer)
