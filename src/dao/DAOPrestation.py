from DAO.DAOSession import DAOSession
from mysql.connector import Error

class DAOPrestation : 

    unique_instance = None

    @staticmethod
    def get_instance() :
        if DAOPrestation.unique_instance is None :
            DAOPrestation.unique_instance = DAOPrestation()
        return DAOPrestation.unique_instance
    
    def insert_Prestation(self, prestation):
        sql = "INSERT INTO Prestation (datePrevue, dateEffective, lieu, type, nbPhotosPrevues, nbVideosPrevues, numeroContrat) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values = (prestation.get_date_prevue(), prestation.get_date_effective(), prestation.get_lieu(), prestation.get_type(), prestation.get_nb_photos_prevues(), prestation.get_nb_videos_prevues(), prestation.get_numero_contrat())
        try : 
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            cle = cursor.lastrowid
            return cle
        except Error as e : 
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Prestation : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback() 
            return -1
        finally:
            if cursor:
                cursor.close()  

    def delete_prestation(self, prestation):
        sql = ""
        pass

    def find_prestation(self, prestation):
        pass

    def update_prestation(self, prestation):
        pass

    def select_prestation(self, prestation):
        pass

    def sett_all_values(self, rs ):
        pass