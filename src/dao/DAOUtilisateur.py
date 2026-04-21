
from dao.DAOSession import DAOSession

from mysql.connector import Error ,InterfaceError, errorcode


class DAOUtilisateur:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOUtilisateur.unique_instance is None:
            DAOUtilisateur.unique_instance = DAOUtilisateur()
        return DAOUtilisateur.unique_instance

    def authentifier(self, email, mot_de_passe):
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

        except InterfaceError as err:
            print("Erreur de connexion : Impossible de se connecter au serveur MySQL.")
            return None
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Erreur d'authentification : Nom d'utilisateur ou mot de passe incorrect.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Erreur de base de données : La base de données spécifiée n'existe pas.")
            elif err.errno == errorcode.ER_PARSE_ERROR:
                print("Erreur de syntaxe dans la requête SQL.")
            elif err.errno == errorcode.ER_NO_SUCH_TABLE:
                print("Erreur : La table spécifiée n'existe pas.")
            else:
                print(f"Erreur inattendue : {err}")
            return None

    @staticmethod
    def get_all_utilisateurs():
        """Récupère tous les utilisateurs actifs"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM Utilisateur WHERE statut = 'ACTIF'"
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
            return True

        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur : {e}")
            return False