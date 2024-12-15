import mysql.connector


def get_mysql_connection(use_pool=False, pool_size=10):
    if use_pool:
        return mysql.connector.connect(
            host="host.docker.internal",
            user="test_user",
            password="test_password",
            pool_size=pool_size,
            pool_name="test",
        )
    return mysql.connector.connect(
        host="host.docker.internal",
        user="test_user",
        password="test_password",
    )
