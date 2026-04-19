from DAO.DAOSession import DAOSession
from mysql.connector import Error

class DAOContrat:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOContrat.unique_instance is None:
            DAOContrat.unique_instance = DAOContrat()
        return DAOContrat.unique_instance

    def insert_contrat(self, contrat):
        sql = "INSERT INTO Contrat (date_debut, duree, nb_productions_totales,periodicite, montant_global, condition_paiements, id_client) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (contrat.get_date_debut(), contrat.get_duree(), contrat.get_nb_productions_totales(), contrat.get_periodicite(), contrat.get_montant_global(), contrat.get_condition_paiements(), contrat.get_id_client())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Contrat : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_contrat(self, contrat):
        pass

    def find_contrat(self, contrat):
        pass

    def update_contrat(self, contrat):
        pass

    def select_contrat(self, contrat):
        pass

    def sett_all_values(self, rs ):
        pass


