from DAO.DAOSession import DAOSession
from mysql.connector import Error

class DAOActivite : 

    unique_instance = None

    @staticmethod
    def get_instance() :
        if DAOActivite.unique_instance is None : 
            DAOActivite.unique_instance = DAOActivite()
        return DAOActivite.unique_instance
    
    def insert_activite(self, activite) :
        sql = "INSERT INTO Activite (libelleOperationnel, datePrevue, dateEffective, dureeEstimeeHeures, responsable, statut, idPrestation) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values = (activite.get_libelle_operationnel(), activite.get_date_prevues(), activite.get_date_effective(), activite.get_duree_estimee(), activite.get_responsable(), activite.get_statut(), activite.get_id_prestation())
        try :
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            cle = cursor.lastrowid
            return cle
        except Error as e : 
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Activite : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback() 
            return -1
        finally:
            if cursor:
                cursor.close()    

    def delete_activite(self, activite):
        sql = ""
        pass

    def find_activite(self, activite):
        pass

    def update_activite(self, activite):
        pass

    def select_activite(self, activite):
        pass

    def sett_all_values(self, rs ):
        pass