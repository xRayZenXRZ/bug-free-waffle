from dao.DAOSession import DAOSession
from mysql.connector import Error
import traceback


class DAOClient:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOClient.unique_instance is None:
            DAOClient.unique_instance = DAOClient()
        return DAOClient.unique_instance

    def insert_client(self, client):
        traceback.print_stack()
        print("Appel insert_client")
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            
            sql = """
                INSERT INTO Client (nom, prenom, raisonSociale, adressePostale, telephone, email, statut)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                client.get_nom(),
                client.get_prenom(),
                client.get_raison_sociale(),
                client.get_adresse(),
                client.get_telephone(),
                client.get_courriel(),
                client.get_status_client()
            ))
            connection.commit()
            cle = cursor.lastrowid
            cursor.close()
            return (True, cle)
        except Exception as e:
            print(f"Erreur lors de la création du Client : {e}")
            return (False, str(e))

    def delete_client(self, client):
        sql = "DELETE FROM Client WHERE idClient = %s"
        values = (client.get_id_client(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du Client : {e}")
            print(sql)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_client(self, client):
        sql = "SELECT * FROM Client WHERE idClient = %s"
        values = (client,)
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
            print(f"Erreur lors de la recherche d'un Client : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_client(self, client):
        sql = "UPDATE Client SET nom = %s, prenom = %s, raisonSociale = %s, adressePostale = %s, telephone = %s, email = %s, statut = %s WHERE idClient = %s"
        values = (client.get_nom(), client.get_prenom(), client.get_raison_sociale(), client.get_adresse(
        ), client.get_telephone(), client.get_courriel(), client.get_status_client(), client.get_id_client())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du Client : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_client(self, client=None):
        les_clients = []
        sql = "SELECT * FROM Client WHERE "

        if client is None:
            sql = "SELECT * FROM Client"
            values = []
        else:
            critere_id_client = client.get_id_client()
            critere_nom = client.get_nom()
            critere_prenom = client.get_prenom()
            critere_raison_sociale = client.get_raison_sociale()
            critere_adresse = client.get_adresse()
            critere_telephone = client.get_telephone()
            critere_courriel = client.get_courriel()
            critere_statut = client.get_status_client()

            values = []

            if critere_id_client is not None and critere_id_client != -1:
                sql += "idClient = %s"
                values.append(critere_id_client)
            elif all(c is None for c in [critere_nom, critere_prenom, critere_raison_sociale, critere_adresse, critere_telephone, critere_courriel, critere_statut]):
                sql = "SELECT * FROM Client"
            else:
                conditions = []
                if critere_nom is not None:
                    conditions.append("nom = %s")
                    values.append(critere_nom)
                if critere_prenom is not None:
                    conditions.append("prenom = %s")
                    values.append(critere_prenom)
                if critere_raison_sociale is not None:
                    conditions.append("raisonSociale = %s")
                    values.append(critere_raison_sociale)
                if critere_adresse is not None:
                    conditions.append("adressePostale = %s")
                    values.append(critere_adresse)
                if critere_telephone is not None:
                    conditions.append("telephone = %s")
                    values.append(critere_telephone)
                if critere_courriel is not None:
                    conditions.append("email = %s")
                    values.append(critere_courriel)
                if critere_statut is not None:
                    conditions.append("statut = %s")
                    values.append(critere_statut)
                sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(values))
            rs = cursor.fetchall()
            for row in rs:
                les_clients.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de Clients : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_clients

    def set_all_values(self, rs):
        from domaine.Client import Client
        client = Client(rs["idClient"], rs["nom"], rs["prenom"], rs["raisonSociale"],
                        rs["adressePostale"], rs["telephone"], rs["email"], rs["statut"])
        return client
