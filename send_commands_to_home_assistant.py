import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost',10000))

while True:
    message = input('Insira um comando no formato [command] [attribute] [device]: ')
    s.send(message.encode('utf-8'))