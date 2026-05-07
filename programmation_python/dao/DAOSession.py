"""Gestion centralisée de la connexion MySQL — un seul objet connexion partagé par tous les DAOs."""

import mysql.connector
from mysql.connector import Error


class DAOSession:
    """Singleton de connexion MySQL. Tous les DAOs passent par DAOSession.get_connexion()."""
    
    # Propriétés statiques
    HOST = "localhost"
    LOGIN = "root"
    MDP = None #password a definir 
    DB="test_comart"
    PORT = 3306
    connection = None

    @staticmethod
    def creer_connection():
        try:
            DAOSession.connection = mysql.connector.connect(
                host=DAOSession.HOST,
                user=DAOSession.LOGIN,
                password=DAOSession.MDP,
                database=DAOSession.DB,
                port=DAOSession.PORT
            )
            if DAOSession.connection.is_connected():
                print("Connexion à la base de données réussie")
            else:
                print("Erreur de connexion à la base")
        except Error as e:
            print(f"Erreur durant la connexion à la base de données: {e}")

    @staticmethod
    def get_connexion():
        if DAOSession.connection is None:
            DAOSession.creer_connection()
        return DAOSession.connection
   
    def open():
        DAOSession.get_connexion().start_transaction()

   
    def close():
        DAOSession.get_connexion().commit()
        DAOSession.get_connexion().close()
        DAOSession.connection = None
        print("Fermeture de la connexion à la base de données")

    @staticmethod
    def clean_database():
        conn = DAOSession.get_connexion()
        cur = conn.cursor()
        for table in ["Activite", "Paiement", "Facture", "Prestation", "Collaborateur", "Devis", "Contrat", "Client"]:
            cur.execute(f"DELETE FROM {table}")
        for table in ["Activite", "Paiement", "Prestation", "Collaborateur", "Client"]:
            cur.execute(f"ALTER TABLE {table} AUTO_INCREMENT = 1")
        conn.commit()
        cur.close()
        print("Base de données nettoyée.")