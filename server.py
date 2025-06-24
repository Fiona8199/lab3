import socket
import threading
import time
from collections import defaultdict

tuple_space = {}
stats = {
    'tuples_count': 0,
    'avg_tuple_size': 0,
    'avg_key_size': 0,
    'avg_value_size': 0,
    'total_clients': 0,
    'total_operations': 0,
    'total_reads': 0,
    'total_gets': 0,
    'total_puts': 0,
    'errors': 0
}def process_request(client_socket, request):
    global stats
    command = request[1]
    key = request[3:].split()[0]
    value = request[3:].split()[1] if command == 'P' else None

    if command == 'P':
        if key in tuple_space:
            client_socket.sendall(f"{len('ERR k already exists')} ERR k already exists".encode())
            stats['errors'] += 1
        else:
            tuple_space[key] = value
            stats['tuples_count'] += 1
            stats['total_operations'] += 1
            stats['total_puts'] += 1
            client_socket.sendall(f"{len(f'OK (k, v) added')} OK (k, v) added".encode())
    elif command == 'R':
        if key in tuple_space:
            stats['total_operations'] += 1
            stats['total_reads'] += 1
            client_socket.sendall(f"{len(f'OK (k, v) read {tuple_space[key]}')} OK (k, v) read {tuple_space[key]}".encode())
        else:
            stats['errors'] += 1
            client_socket.sendall(f"{len('ERR k does not exist')} ERR k does not exist".encode())
    elif command == 'G':
        if key in tuple_space:
            value = tuple_space.pop(key)
            stats['tuples_count'] -= 1
            stats['total_operations'] += 1
            stats['total_gets'] += 1
            client_socket.sendall(f"{len(f'OK (k, v) removed {value}')} OK (k, v) removed {value}".encode())
        else:
            stats['errors'] += 1
            client_socket.sendall(f"{len('ERR k does not exist')} ERR k does not exist".encode())def handle_client(client_socket):
    global stats
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break
        print(f"Received request: {request}")
        response = process_request(client_socket, request)
        client_socket.sendall(response.encode())
    client_socket.close()
    stats['total_clients'] += 1            def start_server(port):
    global stats
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen()
    print(f"Server listening on port {port}")

    while True:
        client_sock, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()                