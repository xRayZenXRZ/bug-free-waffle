from dao.DAOSession import DAOSession
from mysql.connector import Error


class DAOContrat:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOContrat.unique_instance is None:
            DAOContrat.unique_instance = DAOContrat()
        return DAOContrat.unique_instance

    def insert_contrat(self, contrat):
        sql = "INSERT INTO Contrat (numeroContrat ,dateDebut, duree, nbProductionsTotales, periodicite, montantGlobal, conditionsPaiement, idClient) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)"
        values = (contrat.get_numero_contrat(), contrat.get_date_debut(), contrat.get_duree(), contrat.get_nb_productions_totales(
        ), contrat.get_periodicite(), contrat.get_montant_global(), contrat.get_condition_paiements(), contrat.get_id_client())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print("Contrat inséré avec succès !")
            cle = contrat.get_numero_contrat()
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Contrat : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_contrat(self, contrat):
        sql = "DELETE FROM Contrat WHERE numeroContrat = %s"
        values = (contrat.get_numero_contrat(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du Contrat : {e}")
            print(sql)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_contrat(self, contrat):
        sql = "SELECT * FROM Contrat WHERE numeroContrat = %s"
        values = (contrat,)
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
            print(f"Erreur lors de la recherche d'un Contrat : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_contrat(self, contrat):
        sql = "UPDATE Contrat SET dateDebut = %s, duree = %s, nbProductionsTotales = %s, periodicite = %s, montantGlobal = %s, conditionPaiement = %s, idClient = %s WHERE numeroContrat = %s"
        values = (contrat.get_date_debut(), contrat.get_duree(), contrat.get_nb_productions_totales(), contrat.get_periodicite(
        ), contrat.get_montant_global(), contrat.get_condition_paiements(), contrat.get_id_client(), contrat.get_numero_contrat())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du Contrat : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_contrat(self, contrat=None):
        les_contrats = []
        sql = "SELECT * FROM Contrat WHERE "

        if contrat is None:
            sql = "SELECT * FROM Contrat"
            values = []
        else:
            critere_numero_contrat = contrat.get_numero_contrat()
            critere_date_debut = contrat.get_date_debut()
            critere_duree = contrat.get_duree()
            critere_nb_productions = contrat.get_nb_productions_totales()
            critere_periodicite = contrat.get_periodicite()
            critere_montant_global = contrat.get_montant_global()
            critere_condition_paiements = contrat.get_condition_paiements()
            critere_id_client = contrat.get_id_client()

            values = []

            if critere_numero_contrat is not None and critere_numero_contrat != -1:
                sql += "numeroContrat = %s"
                values.append(critere_numero_contrat)
            elif all(c is None for c in [critere_date_debut, critere_duree, critere_nb_productions, critere_periodicite, critere_montant_global, critere_condition_paiements, critere_id_client]):
                sql = "SELECT * FROM Contrat"
            else:
                conditions = []
                if critere_date_debut is not None:
                    conditions.append("dateDebut = %s")
                    values.append(critere_date_debut)
                if critere_duree is not None:
                    conditions.append("duree = %s")
                    values.append(critere_duree)
                if critere_nb_productions is not None:
                    conditions.append("nbProductionsTotales = %s")
                    values.append(critere_nb_productions)
                if critere_periodicite is not None:
                    conditions.append("periodicite = %s")
                    values.append(critere_periodicite)
                if critere_montant_global is not None:
                    conditions.append("montantGlobal = %s")
                    values.append(critere_montant_global)
                if critere_condition_paiements is not None:
                    conditions.append("conditionPaiements = %s")
                    values.append(critere_condition_paiements)
                if critere_id_client is not None:
                    conditions.append("idClient = %s")
                    values.append(critere_id_client)
                sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(values))
            rs = cursor.fetchall()
            for row in rs:
                les_contrats.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de Contrats : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_contrats

    def set_all_values(self, rs):
        from domaine.Contrat import Contrat
        contrat = Contrat(rs["numeroContrat"], rs["dateDebut"], rs["duree"], rs["nbProductionsTotales"],
                          rs["periodicite"], rs["montantGlobal"], rs["conditionsPaiement"], rs["idClient"])
        return contrat
