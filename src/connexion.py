import mysql.connector
from mysql.connector import Error, errorcode, IntegrityError, InterfaceError

print(f" mysql connector version : {mysql.connector.__version__}")

#config

config = {
    "host" : "localhost",
    "port" : "encora à définir",
    "user" : "root",
    "password" : "encore à définir",
    "database" : "encore à définir"
}

