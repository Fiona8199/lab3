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
}