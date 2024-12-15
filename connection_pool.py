import mysql.connector
import time
from helper import get_mysql_connection
import threading


class ConnectionPool:
    connections = []

    def __init__(self, min_pool_size, max_pool_size):
        for i in range(min_pool_size):
            self.connections.append(get_mysql_connection())
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size

    def get_connection(self):

        while not self.connections:
            if len(self.connections) < self.max_pool_size:
                self.connections.append(get_mysql_connection())
            print("waiting to get connection")
            time.sleep(1)
        print("remaining useable connections in pool", len(self.connections) - 1)
        return self.connections.pop()

    def return_connection(self, connection):
        print("remaining useable connections in pool", len(self.connections) + 1)
        self.connections.append(connection)

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.connections = []


def test_custom_connection_pool():
    connection_pool = ConnectionPool(10, 20)
    tasks = []
    start_time = time.time()

    def _benchmark_with_custom_threaded_connection_pool():
        thread_local = threading.local()
        new_connection = connection_pool.get_connection()
        new_connection.ping()
        connection_pool.return_connection(new_connection)
        thread_local.value = threading.current_thread().name
        print("thread name", thread_local.value)

    for i in range(int(100) + 1):
        thread = threading.Thread(
            target=_benchmark_with_custom_threaded_connection_pool,
            name=f"Thread-{i}",
        )
        tasks.append(thread)
        thread.start()
    for thread in tasks:
        thread.join()

    total_time_took = time.time() - start_time
    output = {
        "time_took": total_time_took,
        "range": 100,
        "bench_type": "benchmark_with_custom_threaded_connection_pool",
    }
    print(output)
