import socket

def send_requests(hostname, port, filename):
    with open(filename, 'r') as file:
        requests = file.readlines()