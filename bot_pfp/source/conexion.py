import mysql.connector
from mysql.connector import Error


def conect1():
    try:
        conexion = mysql.connector.connect(
            user='root', password='',
            host='127.0.0.1', database='bot_datos'
            )
        print("Conexión realizada")
        # conexion.close()
        return conexion
    except Error as ex:
        print("Conexión fallida")


if __name__=='__main__':
    None
