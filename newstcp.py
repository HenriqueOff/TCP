import socket
import threading
import psutil # type: ignore

# Lista para manter o registro dos clientes conectados
clientes_conectados = set()  # Usando um set para evitar duplicatas

def gerenciar_cliente(conn, endereco):
    global clientes_conectados
    
    print(f'Cliente conectado de: {endereco}')
    clientes_conectados.add(endereco)
    
    try:
        while True:
            dados = conn.recv(1024)
            if not dados:
                break
            
            mensagem = dados.decode()
            print(f'Dados recebidos de {endereco}: {mensagem}')

            if mensagem == '1':
                resposta = 'Mensagem ecoada.'
            elif mensagem == '2':
                resposta = 'Clientes conectados: ' + ', '.join(map(str, clientes_conectados))
            elif mensagem == '3':
                uso_por_nucleo = psutil.cpu_percent(percpu=True, interval=1)
                # Uso da CPU total
                uso_total = psutil.cpu_percent(interval=1)
                x = 'Os dados do processador do cliente'
                y = 'Uso da CPU por nucleo: {}'.format('\n'.join(map(str, uso_por_nucleo)))
                z = 'O uso total da CPU: {}%'.format(uso_total)
                resposta = '{}\n{}\n{}'.format(x,y,z)

            else:
                resposta = 'Comando não reconhecido.'

            conn.sendall(resposta.encode())
            print(resposta)
    except ConnectionResetError:
        print(f'Conexão com {endereco} foi resetada.')
    finally:
        conn.close()
        clientes_conectados.remove(endereco)
        print(f'Cliente {endereco} desconectado.')

def iniciar_servidor(host, port):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen()
    print(f'Servidor escutando em {host}:{port}')

    while True:
        conn, endereco = servidor.accept()
        thread_cliente = threading.Thread(target=gerenciar_cliente, args=(conn, endereco))
        thread_cliente.start()

if __name__ == '__main__':
    HOST = '192.168.22.20'  # Endereço IP do servidor
    PORT = 50000            # Porta do servidor
    iniciar_servidor(HOST, PORT)
