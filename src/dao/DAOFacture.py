from dao.DAOSession import DAOSession
from mysql.connector import Error

class DAOFacture:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOFacture.unique_instance is None:
            DAOFacture.unique_instance = DAOFacture()
        return DAOFacture.unique_instance

    def insert_facture(self, facture):
        sql = "INSERT INTO Facture (numeroFacture ,dateEmission, montatTotal, etat, numeroContrat) VALUES (%s ,%s, %s, %s, %s)"
        values = (facture.get_date_emission(), facture.get_montant_total(), facture.get_etat(), facture.get_numero_contrat())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            cle = facture.get_numero_facture()
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la Facture : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_facture(self, facture):
        sql = "DELETE FROM Facture WHERE numeroFacture = %s"
        values = (facture.get_numero_facture(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la Facture : {e}")
            print(sql)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_facture(self, facture):
        sql = "SELECT * FROM Facture WHERE numeroFacture = %s"
        values = (facture.get_numero_facture(),)
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
            print(f"Erreur lors de la recherche d'une Facture : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_facture(self, facture):
        sql = "UPDATE Facture SET dateEmission = %s, montatTotal = %s, etat = %s, numeroContrat = %s WHERE numeroFacture = %s"
        values = (facture.get_date_emission(), facture.get_montant_total(), facture.get_etat(), facture.get_numero_contrat(), facture.get_numero_facture())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la Facture : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_facture(self, facture=None):
        les_factures = []
        sql = "SELECT * FROM Facture WHERE "

        if facture is None:
            sql = "SELECT * FROM Facture"
            values = []
        else:
            critere_numero_facture = facture.get_numero_facture()
            critere_date_emission = facture.get_date_emission()
            critere_montant_total = facture.get_montant_total()
            critere_etat = facture.get_etat()
            critere_numero_contrat = facture.get_numero_contrat()

            values = []

            if critere_numero_facture is not None and critere_numero_facture != -1:
                sql += "numeroFacture = %s"
                values.append(critere_numero_facture)
            elif all(c is None for c in [critere_date_emission, critere_montant_total, critere_etat, critere_numero_contrat]):
                sql = "SELECT * FROM Facture"
            else:
                conditions = []
                if critere_date_emission is not None:
                    conditions.append("dateEmission = %s")
                    values.append(critere_date_emission)
                if critere_montant_total is not None:
                    conditions.append("montatTotal = %s")
                    values.append(critere_montant_total)
                if critere_etat is not None:
                    conditions.append("etat = %s")
                    values.append(critere_etat)
                if critere_numero_contrat is not None:
                    conditions.append("numeroContrat = %s")
                    values.append(critere_numero_contrat)
                sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(values))
            rs = cursor.fetchall()
            for row in rs:
                les_factures.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de Factures : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_factures

    def set_all_values(self, rs):
        from domaine.Facture import Facture
        facture = Facture(rs["numeroFacture"], rs["dateEmission"], rs["montatTotal"], rs["etat"], rs["numeroContrat"])
        return facture