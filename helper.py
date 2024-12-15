import mysql.connector


def get_mysql_connection():
    return mysql.connector.connect(
        host="host.docker.internal",
        user="test_user",
        password="test_password",
    )
