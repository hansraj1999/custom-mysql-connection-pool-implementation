from helper import get_mysql_connection
import asyncio
import time


class ConnectionPool:
    def __init__(self, min_pool_size, max_pool_size):
        self.min_pool_size = min_pool_size
        self.max_pool_size = max_pool_size
        self.pool = asyncio.Queue(maxsize=max_pool_size)
        self.current_size = 0  # Tracks total number of connections created
        self.lock = asyncio.Lock()  # Ensures thread-safe incrementing of current_size

    async def initialize_pool(self):
        """Pre-fill the pool with minimum required connections."""
        for _ in range(self.min_pool_size):
            await self._create_new_connection()

    async def _create_new_connection(self):
        async with self.lock:
            if self.current_size < self.max_pool_size:
                connection = get_mysql_connection()
                await self.pool.put(connection)
                self.current_size += 1
                print(f"Created new connection. Current size: {self.current_size}")

    async def get_connection(self):
        """Retrieve a connection from the pool."""
        try:
            connection = await asyncio.wait_for(self.pool.get(), timeout=5)
            print("Acquired connection. Remaining:", self.pool.qsize())
            return connection
        except asyncio.TimeoutError:
            async with self.lock:
                if self.current_size < self.max_pool_size:
                    await self._create_new_connection()
                    connection = await self.pool.get()
                    return connection
            raise Exception("Timeout: No available connections in the pool")

    async def return_connection(self, connection):
        """Return a connection to the pool."""
        try:
            await self.pool.put(connection)
            print("Returned connection. Remaining:", self.pool.qsize())
        except asyncio.QueueFull:
            async with self.lock:
                self.current_size -= 1
            connection.close()
            print("Pool is full. Closed returned connection.")

    async def close_connections(self):
        """Close all connections in the pool."""
        async with self.lock:
            while not self.pool.empty():
                connection = await self.pool.get()
                connection.close()
                self.current_size -= 1
        print("All connections are closed. Pool size reset.")


async def test_custom_async_connection_pool():
    async_connection_pool = ConnectionPool(10, 20)
    await async_connection_pool.initialize_pool()

    async def _benchmark_with_custom_async_connection_pool():
        try:
            new_connection = await async_connection_pool.get_connection()
            new_connection.ping()  # Blocking call, consider replacing with async version if available
            await async_connection_pool.return_connection(new_connection)
        except Exception as e:
            print("Error:", e)

    start_time = time.time()
    tasks = [_benchmark_with_custom_async_connection_pool() for _ in range(100)]
    await asyncio.gather(*tasks)

    total_time_took = time.time() - start_time
    output = {
        "time_took": total_time_took,
        "range": 100,
        "bench_type": "benchmark_with_custom_async_connection_pool",
    }
    print(output)
    return output


if __name__ == "__main__":
    asyncio.run(test_custom_async_connection_pool())
