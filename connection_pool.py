import mysql.connector
import time
from helper import get_mysql_connection
import threading
from queue import LifoQueue, Full, Empty


class ConnectionPool:
    def __init__(self, min_pool_size, max_pool_size):
        self.pool = LifoQueue(maxsize=max_pool_size)
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size

        # Pre-fill the pool with minimum required connections
        for i in range(min_pool_size):
            self.pool.put(get_mysql_connection())

    def get_connection(self):
        try:
            connection = self.pool.get(timeout=5)  # Wait for a connection for 5 seconds
            print("Acquired connection from pool. Remaining:", self.pool.qsize())
            return connection
        except Empty:
            raise Exception("Timeout: No available connections in the pool")

    def return_connection(self, connection):
        try:
            self.pool.put(connection, timeout=5)  # Return connection to the pool
            print("Returned connection to pool. Remaining:", self.pool.qsize())
        except Full:
            connection.close()
            print("Connection pool is full. Closed the returned connection.")

    def close_connections(self):
        while not self.pool.empty():
            connection = self.pool.get()
            connection.close()
        print("All connections are closed.")


def test_custom_connection_pool():
    connection_pool = ConnectionPool(10, 20)
    tasks = []
    start_time = time.time()

    def _benchmark_with_custom_threaded_connection_pool():
        thread_local = threading.local()
        try:
            new_connection = connection_pool.get_connection()
            new_connection.ping()
            connection_pool.return_connection(new_connection)
            thread_local.value = threading.current_thread().name
            print("Thread name:", thread_local.value)
        except Exception as e:
            print("Error in thread:", e)

    for i in range(100):
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


if __name__ == "__main__":
    test_custom_connection_pool()
