import mysql.connector
from mysql.connector import Error

class DAOSession:

    # Propriétés statiques
    HOST = "localhost"
    DB = "test_comart"
    PORT = 3306
    connection = None

    @staticmethod
    def creer_connection(typeConnexion="CLIENT"):
        try:
            # Un seul user MySQL pour l'instant
            user = "root"
            password = "ton_mot_de_passe_root"  # celui de XAMPP, souvent vide ""

            DAOSession.connection = mysql.connector.connect(
                host=DAOSession.HOST,
                user=user,
                password=password,
                database=DAOSession.DB,
                port=DAOSession.PORT
            )
            if DAOSession.connection.is_connected():
                print(f"Connexion réussie en mode {typeConnexion}")

        except Error as e:
            print(f"Erreur de connexion : {e}")

    @staticmethod
    def get_connexion(typeConnexion="CLIENT"):
        if DAOSession.connection is None or not DAOSession.connection.is_connected():
            DAOSession.creer_connection(typeConnexion)
        return DAOSession.connection

    @staticmethod
    def open(typeConnexion="CLIENT"):
        DAOSession.get_connexion(typeConnexion)
        print(f"Transaction démarrée avec le type de connexion: {typeConnexion}")


        
    @staticmethod
    def close():
        if DAOSession.connection is not None and DAOSession.connection.is_connected():
            DAOSession.connection.commit()
            DAOSession.connection.close()
            DAOSession.connection = None