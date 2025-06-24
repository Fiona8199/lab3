import socket

def send_requests(hostname, port, filename):
    with open(filename, 'r') as file:
        requests = file.readlines()    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostname, port))

    for request in requests:
        client.sendall(f"{len(request)} {request}".encode())
        response = client.recv(1024).decode()
        print(f"Response: {response}")

    client.close()if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <filename>")
    else:
        hostname = sys.argv[1]
        port = int(sys.argv[2])
        filename = sys.argv[3]
        send_requests(hostname, port, filename)