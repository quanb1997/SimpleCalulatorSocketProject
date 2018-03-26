import socket
import sys

'''CONFIGURATION'''
LOCAL = '127.0.0.1'
default_ip = '128.119.169.15'
default_port = 52345

operation_codes = b'+',b'-',b'*',b'/'

def operate(operation_code, num1, num2):
    if operation_code not in operation_codes:
        raise OperationError('{} is not a valid operation code. +,-,*,/'.format(operation_code))
    try:
        num1 = int(num1)
    except:
        raise ValueError('Error: Number 1 ({}) is not a valid int!'.format(num1.decode('ascii')))
    try:
        num2 = int(num2)
    except:
        raise ValueError('Error: Number 2 ({}) is not a valid int!'.format(num2.decode('ascii')))

    if operation_code == b'+':
        return 200, num1 + num2
    elif operation_code == b'-':
        return 200, num1 - num2
    elif operation_code == b'*':
        return 200, num1 * num2
    elif operation_code == b'/':
        if num2 == 0:
            raise ZeroDivisionError
        return 200, num1 / num2

class ServerSocket:

    def __init__(self, s = None):
        if s != None:
            self.server_socket = s
        else:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.host = socket.gethostname()
        self.host = 'Server'
        print('{}: Server socket created!'.format(self.host))

    def bind(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket.bind((self.ip, self.port))
        print('{}: Server socket binded to {}:{}'.format(self.host,self.ip, self.port))
        print('-------------------------------------------------------------------------')


    def recv_and_send(self):
        self.server_socket.listen(1)
        print('>Server is listening')
        while True:
            connection_socket, address = self.server_socket.accept()
            print('Connection from {}'.format(address))
            data = connection_socket.recv(1024)
            print('{}: {}'.format(socket.gethostbyaddr(address[0])[0], data))
            data = data.split(b',')
            data = list(filter(lambda x: x != b'', data))
            try:
                print('{}: Computing answer'.format(self.host))
                if len(data) > 3:
                    raise Exception
                ans = operate(data[0],data[1],data[2])
            except:
                err = sys.exc_info()
                err_msg = err[1]
                if len(data) < 3:
                    err_msg = 'Error: Too little input was given.'
                    err_code = 302
                elif err[0] == ValueError:
                    err_code = 301
                elif err[0] == OperationError:
                    err_code = 300
                elif len(data) > 3:
                    err_msg = 'Error: Too much input was given.'
                    err_code = 303
                elif err[0] == ZeroDivisionError:
                    err_code = 304
                else:
                    err_code = 305
                connection_socket.sendto('{},-1'.format(err_code).encode('utf8'), address)
                print('{}: There was an error with the input. {}'.format(self.host, err[1]))
                print('{}: Sent {},-1 to {}\n-------------------------'.format(self.host, err_code, socket.gethostbyaddr(address[0])[0]))
                continue
            ans = str(ans[0]) + ',' + str(ans[1])
            connection_socket.send(ans.encode('utf8'))
            print('{}: Sending {}'.format(self.host,ans))
            connection_socket.close()
            print('--------------------------')
        self.server_socket.close()
        print('Socket Closed!\n---------------------------------')

class OperationError(Exception):
    pass


if __name__ == "__main__":
    ip = default_ip
    port = default_port
    s = ServerSocket()
    s.bind(ip,port)
    s.recv_and_send()
