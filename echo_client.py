import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    buffer_size = 16
    server_address = ('127.0.0.1', 10000)
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print('Connecting to:   {0} on port {1}'.format(*server_address), file=log_buffer)
    print('=' * 50)
    print()
    sock.connect(server_address)
    received_message = ''
    try:
        print('Sending:  "{0}"'.format(msg), file=log_buffer)
        print()
        sock.sendall(msg.encode('utf-8'))
        chunk = sock.recv(buffer_size)
        received_message = chunk
        while len(chunk) == buffer_size:
            chunk = sock.recv(buffer_size)
            received_message += chunk
        print('Received:  "{0}"'.format(received_message.decode('utf8')), file=log_buffer)
        print()

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

    finally:
        print('Closing socket', file=log_buffer)
        print()
        sock.close()
        return received_message.decode('utf8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)