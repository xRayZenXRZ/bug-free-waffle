
from DAO.DAOSession import DAOSession
from mysql.connector import Error

class DAOPAiement : 

    unique_instance = None

    @staticmethod
    def get_instance() :
        if DAOPAiement.unique_instance is None : 
            DAOPAiement.unique_instance = DAOPAiement
        return DAOPAiement.unique_instance
    
    def insert_paiement(self, paiement) : 
        sql = "INSERT INTO Paiement (datePaiement, montantPaye, numeroFacture) VALUES ( %s, %s, %s)"
        values = (paiement.get_date(), paiement.get_montant(), paiement.get_numero_Facture())
        try : 
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Paiement : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback() 
            return -1
        finally:
            if cursor:
                cursor.close()            