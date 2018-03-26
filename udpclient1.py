import socket
import sys
from functools import wraps
import errno
import os
import signal

'''CONFIGURATION'''
default_ip = '172.30.96.109'
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
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.client_socket = s
        self.host = socket.gethostname()
        self.server = socket.gethostbyname(server_ip)
        self.server_ip = server_ip
        self.port = port

    def send_msg(self, msg):
        self.client_socket.sendto(msg.encode('utf8'), (self.server_ip, self.port))
        print('(You){}: {} sent to {}'.format(self.host, msg, self.server))

    def recv_response(self, buffer=1024):
        response = self.client_socket.recvfrom(1024)[0].decode('utf8').split(',')
        status = response[0]
        if status in list(status_codes.keys())[1:]:
            print('(Server){}: [Server Error Code {}] {}'.format(self.server,status, status_codes[status]))
        elif status == '200':
            print('(Server){}: The answer is {}'.format(self.server, response[1]))
        else:
            print(status)
            print('{}: Response recieved: {}'.format(self.server, response))
        self.client_socket.close()
        print('-----------------------------------------------------')
        return self.server, response



try:
    args = sys.argv[1:]
    if len(args) == 0:
        raise Exception
    operation_code = args[0]
    num1 = args[1]
    num2 = args[2]
    client_socket = ClientSocket('192.168.137.1')
    client_socket.send_msg('{},{},{}'.format(operation_code,num1,num2))
    client_socket.recv_response()
except:
    if __name__ == '__main__':

        print('-----------------------------------------------------')
        print('Enter a math question with 2 numbers.\nValid operations: +,-,/,*\nExample: \"+,2,6\" or \"+,6,2\" without the quoteswill return 8')
        while True:
            msg = ''
            try:
                print('Input below. CTRL+C to terminate.')
                operation_code = input('\tOperation: ')
                num1 = input('\tNum1: ')
                num2 = input('\tNum2: ')
                msg += operation_code
                msg += ',' + num1
                msg += ',' + num2
                print('>The server will compute {} {} {}.'.format(num1,operation_code,num2))
                print('-----------------------------------------------------')
            except KeyboardInterrupt:
                raise
            client_socket = ClientSocket()
            client_socket.send_msg(msg)
            try:
                server, response = client_socket.recv_response()
            except Exception as e:
                print('Error: {}.'.format(e))
                print('>quitting program...')
                exit()

def main():
    print('-----------------------------------------------------')
    print('Enter a math question with 2 numbers.\nValid operations: +,-,/,*\nExample: \"+,2,6\" or \"+,6,2\" without the quoteswill return 8')
    while True:
        msg = ''
        try:
            print('Input below. CTRL+C to terminate.')
            operation_code = input('\tOperation: ')
            num1 = input('\tNum1: ')
            num2 = input('\tNum2: ')
            msg += operation_code
            msg += ',' + num1
            msg += ',' + num2
            print('>The server will compute {} {} {}.'.format(num1,operation_code,num2))
            print('-----------------------------------------------------')
        except KeyboardInterrupt:
            raise
        client_socket = ClientSocket()
        client_socket.send_msg(msg)
        try:
            server, response = client_socket.recv_response()
        except:
            print('Error: Server might be down.')
            print('>quitting program...')
            exit()    
