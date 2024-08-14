import socket

def interagir_com_servidor(host, port):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))
    
    while True:
        print("Digite '1' para ecoar uma mensagem.")
        print("Digite '2' para listar clientes conectados.")
        print("Digite '3' para mostrar os dados da sua CPU.")
        print("Digite 'sair' para encerrar o cliente.")
        comando = input("Digite o comando: ")
        
        if comando == 'sair':
            break
        elif comando == '1':
            reposta = input('Digite uma mensagem: ')
        
        cliente.sendall(comando.encode())
        resposta = cliente.recv(1024)
        print('Resposta do servidor:', resposta.decode())

    cliente.close()

if __name__ == '__main__':
    HOST = '192.168.22.20'  # Endereço IP do servidor
    PORT = 50000            # Porta do servidor
    interagir_com_servidor(HOST, PORT)
