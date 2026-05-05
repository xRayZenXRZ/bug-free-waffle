from dao.DAOSession import DAOSession
from mysql.connector import Error


class DAOPaiement:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOPaiement.unique_instance is None:
            DAOPaiement.unique_instance = DAOPaiement()
        return DAOPaiement.unique_instance

    def insert_paiement(self, paiement):
        sql = "INSERT INTO Paiement (datePaiement, montantPaye, numeroFacture) VALUES (%s, %s, %s)"
        values = (paiement.get_date(), paiement.get_montant(),
                  paiement.get_numero_Facture())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            print("paiement inséré avec succès")
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Paiement : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_paiement(self, paiement):
        sql = "DELETE FROM Paiement WHERE idPaiement = %s"
        values = (paiement.get_id_paiement(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du Paiement : {e}")
            print(sql)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_paiement(self, paiement):
        sql = "SELECT * FROM Paiement WHERE idPaiement = %s"
        values = (paiement,)
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
            print(f"Erreur lors de la recherche d'un Paiement : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_paiement(self, paiement):
        sql = "UPDATE Paiement SET datePaiement = %s, montantPaye = %s, numeroFacture = %s WHERE idPaiement = %s"
        values = (paiement.get_date(), paiement.get_montant(),paiement.get_numero_facture(), paiement.get_id_paiement())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du Paiement : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_paiement(self, paiement=None):
        les_paiements = []
        sql = "SELECT * FROM Paiement WHERE "

        if paiement is None:
            sql = "SELECT * FROM Paiement"
            values = []
        else:
            critere_id_paiement = paiement.get_id_paiement()
            critere_date = paiement.get_date()
            critere_montant = paiement.get_montant()
            critere_numero_facture = paiement.get_numero_facture()

            values = []

            if critere_id_paiement is not None and critere_id_paiement != -1:
                sql += "idPaiement = %s"
                values.append(critere_id_paiement)
            elif all(c is None for c in [critere_date, critere_montant, critere_numero_facture]):
                sql = "SELECT * FROM Paiement"
            else:
                conditions = []
                if critere_date is not None:
                    conditions.append("datePaiement = %s")
                    values.append(critere_date)
                if critere_montant is not None:
                    conditions.append("montantPaye = %s")
                    values.append(critere_montant)
                if critere_numero_facture is not None:
                    conditions.append("numeroFacture = %s")
                    values.append(critere_numero_facture)
                sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(values))
            rs = cursor.fetchall()
            for row in rs:
                les_paiements.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de Paiements : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_paiements

    def set_all_values(self, rs):
        from domaine.Paiement import Paiement
        paiement = Paiement(rs["idPaiement"], rs["datePaiement"],
                            rs["montantPaye"], rs["numeroFacture"])
        return paiement
