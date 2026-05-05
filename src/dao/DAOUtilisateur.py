<<<<<<< HEAD
# A completer
from dao.DAOSession import DAOSession
from mysql.connector import Error
import hashlib

class DAOUtilisateur:
=======

from dao.DAOSession import DAOSession
from mysql.connector import Error 


class DAOUtilisateur:

>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOUtilisateur.unique_instance is None:
            DAOUtilisateur.unique_instance = DAOUtilisateur()
        return DAOUtilisateur.unique_instance

<<<<<<< HEAD
    @staticmethod
    def authentifier(email, mot_de_passe):
        """
        Vérifie les identifiants d'un utilisateur
        Retourne les infos utilisateur si trouvé, None sinon
        """
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT idUtilisateur, nom, prenom, email, role, statut 
                FROM Utilisateur 
                WHERE email = %s AND motDePasse = %s AND statut = 'ACTIF'
            """
            cursor.execute(query, (email, mot_de_passe))
            utilisateur = cursor.fetchone()
            cursor.close()
            return utilisateur  # None si pas trouvé
        except Exception as e:
            print(f"Erreur lors de l'authentification : {e}")
            return None
        
    @staticmethod
    def authentifier_hash(email, mot_de_passe):
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT idUtilisateur, nom, prenom, motDePasse , email, role, statut FROM Utilisateur WHERE email = %s"

            cursor.execute(query, (email,))
            utilisateur = cursor.fetchone()

            if utilisateur is None:
                return None  # Email introuvable

            hache_stocke = hashlib.sha256(utilisateur['motDePasse'].strip().encode()).hexdigest()
            hache_saisi  = hashlib.sha256(mot_de_passe.strip().encode()).hexdigest()

            print(f"hash saisi : {hache_saisi} | hash stocké : {hache_stocke}")

            cursor.close()
            return utilisateur if hache_saisi == hache_stocke else None

        except Exception as e:
            print(f"Erreur lors de l'authentification : {e}")
            return None

    @staticmethod
    def get_all_utilisateurs():
        """Récupère tous les utilisateurs"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM Utilisateur"
            cursor.execute(query)
            utilisateurs = cursor.fetchall()
            cursor.close()
            return utilisateurs
        except Exception as e:
            print(f"Erreur lors de la récupération des utilisateurs : {e}")
            return []

    @staticmethod
    def creer_utilisateur(nom, prenom, email, mot_de_passe, role, id_createur):
        """Crée un nouvel utilisateur (pour les admins)"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor()
            query = """
                INSERT INTO Utilisateur (nom, prenom, email, motDePasse, role, idCreateur)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nom, prenom, email,
                                   mot_de_passe, role, id_createur))
            conn.commit()
            cursor.close()
            return (True, None)
        except Exception as e:
            error_message = str(e)
            print(
                f"Erreur lors de la création de l'utilisateur : {error_message}")

            # Analyser l'erreur pour donner un message plus clair
            if "Duplicate entry" in error_message and "email" in error_message:
                return (False, "Cet email est déjà utilisé")
            elif "Duplicate entry" in error_message:
                return (False, "Cette donnée existe déjà")
            else:
                return (False, f"Erreur BDD : {error_message}")

    @staticmethod
    def desactiver_utilisateur(id_utilisateur):
        """Désactive un utilisateur (soft delete)"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor()
            # Soft delete : on passe le statut à INACTIF
            query = "UPDATE Utilisateur SET statut = 'INACTIF' WHERE idUtilisateur = %s"
            cursor.execute(query, (id_utilisateur,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
            return False

    @staticmethod
    def activer_utilisateur(id_utilisateur):
        """Activer un utilisateur"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor()
            # On passe le statut à Actif
            query = "UPDATE Utilisateur SET statut = 'Actif' WHERE idUtilisateur = %s"
            cursor.execute(query, (id_utilisateur,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
            return False

    @staticmethod
    def supprimer_utilisateur(id_utilisateur):
        """Désactive un utilisateur (soft delete)"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor()
            # Soft delete : on passe le statut à INACTIF
            query = "DELETE FROM Utilisateur WHERE idUtilisateur = %s"
            cursor.execute(query, (id_utilisateur,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")
            return False
=======
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
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357
