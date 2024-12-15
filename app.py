from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from connection_pool import ConnectionPool
from async_connection_pool import ConnectionPool as AsyncConnectionPool
import socket
from helper import get_mysql_connection
import mysql.connector
import time
import threading
import asyncio
from contextlib import asynccontextmanager


def start_server():
    connections = {}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        connections["sync_connection_pool"] = ConnectionPool(10, 20)
        connections["async_connection_pool"] = AsyncConnectionPool(10, 20)
        connections["inbuilt_connection_pool"] = get_mysql_connection(use_pool=True)
        print("created connections")
        yield
        print("closing connections")
        connections["sync_connection_pool"].close_connections()
        connections["async_connection_pool"].close_connections()
        connections["inbuilt_connection_pool"].close()

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def home():
        print(socket.gethostname())
        return {"home_page": f"hello {socket.gethostname()}"}

    @app.get("/benchmark/without_connection_pool")
    async def benchmark_without_pool(_range=100):
        start_time = time.time()
        for i in range(int(_range) + 1):
            new_connection = get_mysql_connection()
            new_connection.ping()

        total_time_took = time.time() - start_time
        output = {
            "time_took": total_time_took,
            "range": _range,
            "bench_type": "without_connection_pool",
        }
        print(output)
        return output

    @app.get("/benchmark/with_inbuilt_connection_pool")
    async def benchmark_with_inbuilt_connection_pool(_range=100):
        start_time = time.time()
        for i in range(int(_range) + 1):
            new_connection = connections["inbuilt_connection_pool"]
            new_connection.ping()

        total_time_took = time.time() - start_time
        output = {
            "time_took": total_time_took,
            "range": _range,
            "bench_type": "with_inbuilt_connection_pool",
        }
        print(output)
        return output

    def _benchmark_with_custom_threaded_connection_pool():
        thread_local = threading.local()
        new_connection = connections["sync_connection_pool"].get_connection()
        new_connection.ping()
        connections["sync_connection_pool"].return_connection(new_connection)
        thread_local.value = threading.current_thread().name
        print("thread name", thread_local.value)

    @app.get("/benchmark/with_custom_connection_pool")
    async def benchmark_with_custom_threaded_connection_pool(_range=100):
        start_time = time.time()
        tasks = []
        for i in range(int(_range) + 1):
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
            "range": _range,
            "bench_type": "benchmark_with_custom_threaded_connection_pool",
        }
        print(output)
        return output

    async def _benchmark_with_custom_async_threaded_connection_pool():
        new_connection = await connections["async_connection_pool"].get_connection()
        new_connection.ping()
        await connections["async_connection_pool"].return_connection(new_connection)

    @app.get("/benchmark/with_custom_async_connection_pool")
    async def benchmark_with_custom_async_connection_pool(_range=100):
        start_time = time.time()
        tasks = []
        for i in range(int(_range) + 1):
            tasks.append(_benchmark_with_custom_async_threaded_connection_pool())
        await asyncio.gather(*tasks)
        total_time_took = time.time() - start_time
        output = {
            "time_took": total_time_took,
            "range": _range,
            "bench_type": "benchmark_with_custom_async_connection_pool",
        }
        print(output)
        return output

    return app
