import socket
import sys

'''CONFIGURATION'''
LOCAL = '127.0.0.1'
default_ip = None
default_port = 52345


operation_codes = '+','-','*','/'

status_codes = {
    '200':'OK',
    '300':'Given operation is not a valid operation code. +,-,*,/ !',
    '301':'Either number input was not an integer!',
    '302':'Too little input was given.',
    '303':'Too many operations requested! Can only do one at a time.',
    '304':'Cannot divide by zero!',
    '305':'Unidentified error.'
}

class OperationError(Exception):
    pass

class ClientSocket:

    def __init__(self, server_ip=default_ip, port=default_port, s=None):
        self.host = socket.gethostname()
        if s == None:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.client_socket = s
        self.host = 'You'
        self.server = 'Server'
        self.server_ip = server_ip
        self.port = port

    def connect(self):
        print('Establishing connection...')
        try:
            self.client_socket.connect((self.server_ip, self.port))
        except Exception as e:
            print('Failed to establish a connection!')
            print(e)
            input('\n>>>enter anything to quit')
            exit()
        print('Connection made with {}!'.format(self.server_ip))


    def send_msg(self, msg):
        self.client_socket.send(msg.encode('utf8'))
        print('{}: {} sent to {}'.format(self.host, msg, socket.gethostbyaddr(self.server_ip)[0]))

    def close(self):
        client_socket.close()
        return True


    def recv_response(self, buffer=1024):
        response = self.client_socket.recv(1024).decode('utf8').split(',')
        status = response[0]
        if status in list(status_codes.keys())[1:]:
            print('Server Error Code {}: {}'.format(status, status_codes[status]))
        elif status == '200':
            print('{}: The answer is {}'.format(self.server, response[1]))
        else:
            print(status)
            print('{}: Response recieved: {}'.format(self.server, response))
        print('-----------------------------------------------------')
        return self.server, response



if __name__ == '__main__':
    if default_ip == None:
        print('set the ip in the configuration')
        input('enter anything to continue')
        exit()
    print('-----------------------------------------------------')
    
    while True:
        client_socket = ClientSocket()
        client_socket.connect()
        print('Enter a math question with 2 numbers.\nValid operations: +,-,/,*')
        msg = ''
        try:
            print('Input below. press ctrl+c to quit')
            operation_code = input('\tOperation: ')
            if operation_code == 'exit' or operation_code == '\'exit\'':
                client_socket.client_socket.close()
                print("Connection closed through exit command")
                exit()
            num1 = input('\tNum1: ')
            num2 = input('\tNum2: ')
            msg += operation_code
            msg += ',' + num1
            msg += ',' + num2
            print('>The server will compute {} {} {}.'.format(num1,operation_code,num2))
            print('-----------------------------------------------------')
        except KeyboardInterrupt:
            client_socket.client_socket.close()
            print('Connection Closed!')
        client_socket.send_msg(msg)
        server, response = client_socket.recv_response()
