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
            # Définir les identifiants en fonction du type de connexion
            if typeConnexion == "CLIENT":
                user = "Abonne"
                password = DAOSession.MDP
            elif typeConnexion == "ADMIN":
                user = "Gestionnaire"
                password = DAOSession.MDP
            else:
                raise ValueError("Type de connexion invalide. Utilisez 'CLIENT' ou 'ADMIN'.")

            # Établir la connexion
            DAOSession.connection = mysql.connector.connect(
                host=DAOSession.HOST,
                user=user,
                password=password,
                database=DAOSession.DB,
                port=DAOSession.PORT
            )

            if DAOSession.connection.is_connected():
                print(f"Connexion à la base de données réussie (utilisateur: {user})")
            else:
                print("Erreur de connexion à la base")

        except Error as e:
            print(f"Erreur durant la connexion à la base de données: {e}")
        except ValueError as ve:
            print(f"Erreur: {ve}")

    @staticmethod
    def get_connexion(typeConnexion=None):
        if DAOSession.connection is None:
            DAOSession.creer_connection(typeConnexion)
        return DAOSession.connection

    @staticmethod
    def open(typeConnexion="abonné"):
        DAOSession.get_connexion(typeConnexion).start_transaction()
        print(f"Transaction démarrée avec le type de connexion: {typeConnexion}")

    @staticmethod
    def close():
        if DAOSession.connection is not None:
            DAOSession.get_connexion().commit()
            DAOSession.get_connexion().close()
            DAOSession.connection = None
            print("Fermeture de la connexion à la base de données")