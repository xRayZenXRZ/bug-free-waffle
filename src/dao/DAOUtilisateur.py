
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
            sql = "INSERT INTO Utilisateur (email, motDePasse, typeUtilisateur, idClient) VALUES (%s, %s, %s, %s)"
            valeurs = (compte.get_email(), compte.get_motDePasse(), compte.get_typeUtilisateur(), None)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            print("Utilisateur inséré avec succès")
            cle = cursor.lastrowid
            connection.commit()
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
        sql = "SELECT * FROM Utilisateur WHERE email = %s AND motDePasse = %s"
        valeurs = (email, motDePasse)
        cursor = None
        try:
            connection = DAOSession.get_connexion()

            if connection is None or not connection.is_connected():
                raise RuntimeError("La connexion à la base de données n'est pas ouverte ou est invalide.")

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
            print(f"Requête SQL : {sql}")
            print(f"Valeurs : {valeurs}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def set_all_values(self, rs):
        from domaine.Utilisateur import Utilisateur
        compte = Utilisateur(rs['idUtilisateur'], rs['email'], rs['motDePasse'], rs['typeUtilisateur'])
        if rs['typeUtilisateur'] == "CLIENT":
            from domaine.Client import Client
            compte.set_client(Client.charger(rs['idClient']))
        return compte