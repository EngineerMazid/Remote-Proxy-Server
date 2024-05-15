import socket
import threading

proxy_host = '0.0.0.0'
proxy_port = 8080

def handle_client(client_socket):

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect(('178.153.208.0', 26343))

    while True:

        data = client_socket.recv(4096)
        if not data:
            break

        remote_socket.send(data)

        remote_response = remote_socket.recv(4096)

        client_socket.send(remote_response)

    remote_socket.close()
    client_socket.close()

proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server.bind((proxy_host, proxy_port))
proxy_server.listen(5)

print(f"[*] Proxy server listening on {proxy_host}:{proxy_port}")

while True:
    client_socket, client_addr = proxy_server.accept()
    print(f"[*] Accepted connection from {client_addr[0]}:{client_addr[1]}")

    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
