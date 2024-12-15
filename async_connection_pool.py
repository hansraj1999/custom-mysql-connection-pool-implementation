import mysql.connector
from helper import get_mysql_connection
import asyncio
import time


class CustomAsyncConnectionPool:
    connections = []

    def __init__(self, min_pool_size, max_pool_size):
        for i in range(min_pool_size):
            self.connections.append(get_mysql_connection())
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size

    async def get_connection(self):

        while not self.connections:
            if len(self.connections) < self.max_pool_size:
                self.connections.append(get_mysql_connection())
            print("waiting to get connection")
            await asyncio.sleep(1)
        print("remaining useable connections in pool", len(self.connections) - 1)
        return self.connections.pop()

    async def return_connection(self, connection):
        print("remaining useable connections in pool", len(self.connections) + 1)
        self.connections.append(connection)

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.connections = []


async def test_custom_async_connection_pool():
    async_connection_pool = CustomAsyncConnectionPool(10, 20)

    async def _benchmark_with_custom_async_threaded_connection_pool():
        new_connection = await async_connection_pool.get_connection()
        new_connection.ping()
        await async_connection_pool.return_connection(new_connection)

    start_time = time.time()
    tasks = []
    for i in range(int(100) + 1):
        tasks.append(_benchmark_with_custom_async_threaded_connection_pool())
    await asyncio.gather(*tasks)
    total_time_took = time.time() - start_time
    output = {
        "time_took": total_time_took,
        "range": 100,
        "bench_type": "benchmark_with_custom_async_connection_pool",
    }
    print(output)
    return output
