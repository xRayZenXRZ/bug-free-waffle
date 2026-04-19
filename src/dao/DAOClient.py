from DAO.DAOSession import DAOSession
from mysql.connector import Error

class DAOClient :

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOClient.unique_instance is None :
            DAOClient.unique_instance = DAOClient()
        return DAOClient.unique_instance

    def insert_client(self, client) :
        sql = "INSERT INTO Client (nom, prenom, raisonSociale, adressePostale, telephone, email, statut) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (client.get_nom(), client.get_prenom() , client.get_raison_sociale(), client.get_adresse(), client.get_telephone(), client.get_courriel(), client.get_status_client())
        try :
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Client : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback() 
            return -1
        finally:
            if cursor:
                cursor.close()
    
    def delete_client(self, client):
        sql = ""
        pass

    def find_client(self, client):
        pass

    def update_client(self, client):
        pass

    def select_client(self, client):
        pass

    def sett_all_values(self, rs ):
        pass