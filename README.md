# Custom MySQL Connection Pool Implementation

This repository contains a comprehensive implementation of custom MySQL connection pools (both synchronous and asynchronous) for FastAPI. It also includes benchmarking routes to evaluate the performance of different connection pool strategies.

# Features

-   **Threaded Connection Pool**
    
-   **Asynchronous Connection Pool**
    
-   **Inbuilt MySQL Connection Pool**
    
-   **Benchmarking Endpoints***


## Installing
	1. Install Docker.
	2. Run the following command: docker-compose up

## Usage

Access the FastAPI Swagger documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
## API Endpoints

### **Benchmark Without Connection Pool**

**GET**  `/benchmark/without_connection_pool`

-   **Query Parameter:**  `_range` (default: 100) - Number of iterations to run.
    
-   **Description:** Benchmarks MySQL queries without using any connection pool.
    

### **Benchmark With Inbuilt Connection Pool**

**GET**  `/benchmark/with_inbuilt_connection_pool`

-   **Query Parameter:**  `_range` (default: 100) - Number of iterations to run.
    
-   **Description:** Benchmarks MySQL queries using MySQL's inbuilt connection pool.
    

### **Benchmark With Custom Threaded Connection Pool**

**GET**  `/benchmark/with_custom_threaded_connection_pool`

-   **Query Parameter:**  `_range` (default: 100) - Number of iterations to run.
    
-   **Description:** Benchmarks MySQL queries using a custom Threaded connection pool.
    

### **Benchmark With Custom Asynchronous Connection Pool**

**GET**  `/benchmark/with_custom_async_connection_pool`

-   **Query Parameter:**  `_range` (default: 100) - Number of iterations to run.
    
-   **Description:** Benchmarks MySQL queries using a custom asynchronous connection pool.## API Endpoints

### **Benchmark Without Connection Pool**

**GET**  `/benchmark/without_connection_pool`

-   **Query Parameter:**  `_range` (default: 100) - Number of iterations to run.
    
-   **Description:** Benchmarks MySQL queries without using any connection pool

## Benchmarking

You can evaluate the performance of different connection pool strategies by calling the endpoints mentioned in the API Endpoints section.

> curl -X 'GET' 'http://localhost:8000/benchmark/without_connection_pool?_range=100' -H 'accept: application/json'

-> { "time_took": 3.8543057441711426, "range": "100", "bench_type": "without_connection_pool" }

> curl -X 'GET' 'http://localhost:8000/benchmark/with_inbuilt_connection_pool?_range=100' -H 'accept: application/json'

-> { "time_took": 1.1707117557525635, "range": "100", "bench_type": "with_custom_threaded_connection_pool" }
> curl -X 'GET' 'http://localhost:8000/benchmark/with_custom_threaded_connection_pool?_range=100' -H 'accept: application/json'

->{ "time_took": 0.12557268142700195, "range": "100", "bench_type": "benchmark_with_custom_threaded_connection_pool" }

> curl -X 'GET' 'http://localhost:8000/benchmark/with_custom_async_connection_pool?_range=100' -H 'accept: application/json'

-> { "time_took": 0.1372232437133789, "range": "100", "bench_type": "benchmark_with_custom_async_connection_pool" }
