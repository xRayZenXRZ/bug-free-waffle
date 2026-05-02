from dao.DAOSession import DAOSession
from mysql.connector import Error
import traceback


class DAOCollaborateur:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOCollaborateur.unique_instance is None:
            DAOCollaborateur.unique_instance = DAOCollaborateur()
        return DAOCollaborateur.unique_instance

    def insert_collaborateur(self, collaborateur):
        traceback.print_stack()
        print("Appel insert_collaborateur")
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()

            sql = """
                INSERT INTO Collaborateur (nom, prenom, poste, telephonePro, numeroDevis, idUtilisateur)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                collaborateur.get_nom(),
                collaborateur.get_prenom(),
                collaborateur.get_poste(),
                collaborateur.get_telephone_pro(),
                collaborateur.get_numero_devis(),
                collaborateur.get_id_utilisateur(),
            ))
            connection.commit()
            cle = cursor.lastrowid
            cursor.close()
            return (True, cle)
        except Exception as e:
            print(f"Erreur lors de la création du Collaborateur : {e}")
            return (False, str(e))

    def delete_collaborateur(self, collaborateur):
        sql = "DELETE FROM Collaborateur WHERE idCollaborateur = %s"
        values = (collaborateur.get_id_collaborateur(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du Collaborateur : {e}")
            print(sql)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_collaborateur(self, id_collaborateur):
        sql = "SELECT * FROM Collaborateur WHERE idCollaborateur = %s"
        values = (id_collaborateur,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, values)
            rs = cursor.fetchone()
            if rs:
                return self.set_all_values(rs)
            else:
                return None
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'un Collaborateur : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_collaborateur(self, collaborateur):
        sql = """
            UPDATE Collaborateur
            SET nom = %s, prenom = %s, poste = %s, telephonePro = %s,
                numeroDevis = %s, idUtilisateur = %s
            WHERE idCollaborateur = %s
        """
        values = (
            collaborateur.get_nom(),
            collaborateur.get_prenom(),
            collaborateur.get_poste(),
            collaborateur.get_telephone_pro(),
            collaborateur.get_numero_devis(),
            collaborateur.get_id_utilisateur(),
            collaborateur.get_id_collaborateur(),
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du Collaborateur : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_collaborateur(self, collaborateur=None):
        les_collaborateurs = []
        sql = "SELECT * FROM Collaborateur WHERE "

        if collaborateur is None:
            sql = "SELECT * FROM Collaborateur"
            values = []
        else:
            critere_id_collaborateur = collaborateur.get_id_collaborateur()
            critere_nom              = collaborateur.get_nom()
            critere_prenom           = collaborateur.get_prenom()
            critere_poste            = collaborateur.get_poste()
            critere_numero_devis     = collaborateur.get_numero_devis()
            critere_telephone_pro    = collaborateur.get_telephone_pro()
            critere_id_utilisateur   = collaborateur.get_id_utilisateur()

            values = []

            if critere_id_collaborateur is not None and critere_id_collaborateur != -1:
                sql += "idCollaborateur = %s"
                values.append(critere_id_collaborateur)
            elif all(c is None for c in [critere_nom, critere_prenom, critere_poste, critere_numero_devis ,critere_telephone_pro, critere_id_utilisateur]):
                sql = "SELECT * FROM Collaborateur"
            else:
                conditions = []
                if critere_nom is not None:
                    conditions.append("nom = %s")
                    values.append(critere_nom)
                if critere_prenom is not None:
                    conditions.append("prenom = %s")
                    values.append(critere_prenom)
                if critere_numero_devis is not None:
                    conditions.append("numeroDevis = %s")
                    values.append(critere_numero_devis)
                if critere_poste is not None:
                    conditions.append("poste = %s")
                    values.append(critere_poste)
                if critere_telephone_pro is not None:
                    conditions.append("telephonePro = %s")
                    values.append(critere_telephone_pro)
                if critere_id_utilisateur is not None:
                    conditions.append("idUtilisateur = %s")
                    values.append(critere_id_utilisateur)
                sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(values))
            rs = cursor.fetchall()
            for row in rs:
                les_collaborateurs.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de Collaborateurs : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_collaborateurs

    def set_all_values(self, rs):
        from domaine.Collaborateur import Collaborateur
        collaborateur = Collaborateur(
            id_collaborateur=rs["idCollaborateur"],
            nom=rs["nom"],
            prenom=rs["prenom"],
            poste=rs["poste"],
            telephone_pro=rs["telephonePro"],
            numero_devis=rs["numeroDevis"],
            id_utilisateur=rs["idUtilisateur"],
        )
        return collaborateur