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
        sql = "DELETE FROM Activite WHERE idActivite = %s"
        values = (activite.get_id_activite(),)
        try :
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e : 
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de activite : {e}")
            print(sql)
            print("rollback")
            connection.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()


    def find_activite(self, activite):
        sql = "SELECT * FROM Activite WHERE idActivite = %s"
        values = (activite.get_id_activite())
        try : 
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql,values)
            rs = cursor.fetchone()
            if rs :
                return self.sett_all_values(rs)
            else : 
                return None
        except Error as e : 
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'un activite : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_activite(self, activite):
        sql = "UPDATE Activite SET libelleOperationnel = %s, datePrevue = %s, dateEffective = %s , dureeEstimeeHeures= %s, responsable = %s, statut = %s, idPrestation = %s WHERE idActivite = %s"
        valeurs = (activite.get_libelle_operationnel(), activite.get_date_prevues(), activite.get_date_effective(), activite.get_duree_estimee(), activite.get_responsable(), activite.get_statut(), activite.get_id_prestation(), activite.get_id_activite())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de activite : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return False
        finally:
            if cursor:
                cursor.close()        


    def select_activite(self, activite):

        les_activites = []

        sql = "SELECT * FROM Activite WHERE "
        critere_id_activite = activite.get_id_activite()
        critere_libelle_operationnel = activite.get_libelle_operationnel()
        critere_date_prevues = activite.get_date_prevues()
        critere_date_effective = activite.get_date_effective()
        critere_duree_estimee = activite.get_duree_estimee()
        critere_responsable = activite.get_responsable()
        critere_statut = activite.get_statut()
        critere_id_prestation = activite.get_id_prestation()

        values = []

        if (critere_id_activite is not None) and (critere_id_activite!=-1):
            sql += "idActivite = %s"
            values.append(critere_id_activite)
        elif (critere_libelle_operationnel and critere_date_prevues and critere_date_effective and critere_duree_estimee and critere_responsable and critere_statut and critere_id_prestation) is None :
            sql = "SELECT * FROM Activite"
        else:
            conditions = []
            if critere_libelle_operationnel is not None:
                conditions.append("libelleOperationnel = %s")
                values.append(critere_libelle_operationnel)

            if critere_date_prevues is not None:
                conditions.append("datePrevue = %s")
                values.append(critere_date_prevues)

            if critere_date_effective is not None:
                conditions.append("dateEffective = %s")
                values.append(critere_date_effective)

            if critere_duree_estimee is not None:
                conditions.append("dureeEstimeeHeures = %s")
                values.append(critere_duree_estimee)

            if critere_responsable is not None:
                conditions.append("responsable = %s")
                values.append(critere_responsable)

            if critere_statut is not None : 
                conditions.append("statut = %s")
                values.append(critere_statut)

            if critere_id_prestation is not None :
                conditions.append("idPrestation = %s")
                values.append(critere_id_prestation)

            sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(values))
            rs = cursor.fetchall()
            for row in rs:
                les_activites.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de activite : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_activites

    def set_all_values(self, rs):
        from domaine.Activite import Activite
        activite = Activite(rs["idActivite"], rs["libelleOperationnel"], rs["datePrevue"], rs["dateEffective"], rs["dureeEstimeeHeures"], rs["responsable"], rs["statut"], rs["idPrestation"])
        return activite