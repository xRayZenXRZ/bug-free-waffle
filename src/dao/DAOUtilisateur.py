# A completer
from dao.DAOSession import DAOSession
from mysql.connector import Error


class DAOUtilisateur:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOUtilisateur.unique_instance is None:
            DAOUtilisateur.unique_instance = DAOUtilisateur()
        return DAOUtilisateur.unique_instance

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
