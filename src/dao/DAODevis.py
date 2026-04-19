from DAO.DAOSession import DAOSession
from mysql.connector import Error

class DAODevis :

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAODevis.unique_instance is None:
            DAODevis.unique_instance = DAODevis()
        return DAODevis.unique_instance
    
    def insert_devis(self, devis):
        sql = "INSERT INTO Devis ( dateEmission, dateValidite, descriptionPrestation, quantitePrevue, detailsCouts, montantTotalEstime, statut, dateAcceptation, idClient, numeroContrat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = ( devis.get_date_emission(), devis.get_date_validite(), devis.get_description_prestation(), devis.get_quantite_prevue(), devis.get_details_couts(), devis.get_montant_total_estime(), devis.get_statut(), devis.get_date_acceptation(), devis.get_id_client(), devis.get_numero_contrat())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            cle = cursor.lastrowid
            connection.commit()
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Devis : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_devis(self, devis):
        sql = ""
        pass

    def find_devis(self, devis):
        pass

    def update_devis(self, devis):
        pass

    def select_devis(self, devis):
        pass

    def sett_all_values(self, rs ):
        pass
        
    