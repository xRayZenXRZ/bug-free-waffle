from DAO.DAOSession import DAOSession
from mysql.connector import Error


class DAOFacture : 

    unique_instance = None

    @staticmethod
    def get_instance() :
        if DAOFacture.unique_instance is None :
            DAOFacture.unique_instance = DAOFacture()
        return DAOFacture.unique_instance
    
    def insert_facture(self, facture) : 
        sql = "INSERT INTO Facture (dateEmission, montatTotal, etat, numeroContrat) VALUES (%s, %s, %s, %s)"
        values = (facture.get_date_emission(), facture.get_montant_total(), facture.get_etat(), facture.get_numero_contrat()) #verifier les getters après modifications.
        try :
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            cle = cursor.lastrowid
            return cle
        
        except Error as e :
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Facture : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return -1
        finally : 
            if cursor : 
                cursor.close()

    def delete_facture(self, facture):
        sql = ""
        pass

    def find_facture(self, facture):
        pass

    def update_facture(self, facture):
        pass

    def select_facture(self, facture):
        pass

    def sett_all_values(self, rs ):
        pass