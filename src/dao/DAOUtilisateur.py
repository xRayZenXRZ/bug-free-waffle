
from dao.DAOSession import DAOSession
from mysql.connector import Error 


class DAOUtilisateur:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOUtilisateur.unique_instance is None:
            DAOUtilisateur.unique_instance = DAOUtilisateur()
        return DAOUtilisateur.unique_instance

    def insert_compte(self, compte):
        if compte.get_client() is not None:
            sql = "INSERT INTO Utilisateur (email, motDePasse, typeUtilisateur, idClient) VALUES (%s, %s, %s, %s)"
            valeurs = (compte.get_email(), compte.get_motDePasse(), compte.get_typeUtilisateur(), compte.get_client().get_id_client())
        else:
            # print("compte administrateur")
            sql = "INSERT INTO Utilisateur (email, motDePasse, typeUtilisateur, idClient) VALUES (%s, %s, %s, %s)"
            valeurs = (compte.get_email(), compte.get_motDePasse(), compte.get_typeUtilisateur(), None)
        # print(sql)
        # print(valeurs)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            print("Utilisateur inséré avec succès")
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de compte utilisateur : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback() 
            return -1
        finally:
            if cursor:
                cursor.close()    


    def find_by_email_motDePasse(self, email, motDePasse):
        sql = "SELECT * FROM compteUtilisateur WHERE email = %s AND motDePasse = %s"
        valeurs = (email, motDePasse)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, valeurs)
            result = cursor.fetchone()
            if result:
                return self.set_all_values(result) 
            else:
                return None
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de compte utilisateur : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

"""    def set_all_values(self, rs):
            from domaine.Utilisateur import Utilisateur
            un_compte = Utilisateur(rs['iUtilisateur'], rs['email'], rs['motDePasse'], rs['typeUtilisateur'])
            if rs['typeCompte'] == "abonné":
                from domaine.Client import Client
                un_compte.set_client(Client.charger(rs['idClient']))    
            return un_compte"""
