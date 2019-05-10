import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    buffer_size = 16
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('Waiting for a connection', file=log_buffer)
            print()
            conn, addr = sock.accept()
            print('Connection established at: - {0}:{1}'.format(*addr), file=log_buffer)
            print('=' * 50, '\n')
            try:
                chunk = conn.recv(buffer_size)
                data = chunk
                # print(len(chunk))
                while len(chunk) == buffer_size:
                    chunk = conn.recv(buffer_size)
                    data += chunk

                print('Received: "{0}"'.format(data.decode('utf8')))
                print()
                print('Sending back: "{0}"'.format(data.decode('utf8')))
                conn.sendall(data)

            except Exception as e:
                traceback.print_exc(e)
                sys.exit(1)

            finally:
                conn.close()
                print()
                print('Echo complete, client connection closed', file=log_buffer)
                print()
        
        sock.close()

    except KeyboardInterrupt:
        print('   "Ctrl+C" entered: Exiting echo server', file=log_buffer)
        print()
        sock.close()

if __name__ == '__main__':
    server()
    sys.exit(0)