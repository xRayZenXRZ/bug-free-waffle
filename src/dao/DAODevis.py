from dao.DAOSession import DAOSession
from mysql.connector import Error


class DAODevis:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAODevis.unique_instance is None:
            DAODevis.unique_instance = DAODevis()
        return DAODevis.unique_instance

    def insert_devis(self, devis):
        sql = "INSERT INTO Devis (numeroDevis ,dateEmission, dateValidite, descriptionPrestation, quantitePrevue, detailsCouts, montantTotalEstime, statut, dateAcceptation, idClient, numeroContrat) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (devis.get_numero_devis(), devis.get_date_emission(), devis.get_date_validite(), devis.get_description_prestation(), devis.get_quantite_prevue(
        ), devis.get_details_couts(), devis.get_montant_total_estime(), devis.get_statut(), devis.get_date_acceptation(), devis.get_id_client(), devis.get_numero_contrat())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print("Devis inséré avec succès !")
            cle = devis.get_numero_contrat()
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du Devis : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_devis(self, devis):
        sql = "DELETE FROM Devis WHERE numeroDevis = %s"
        values = (devis.get_numero_devis(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du Devis : {e}")
            print(sql)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_devis(self, devis):
        sql = "SELECT * FROM Devis WHERE numeroDevis = %s"
        values = (devis.get_numero_devis(),)
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
            print(f"Erreur lors de la recherche d'un Devis : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_devis(self, devis):
        sql = "UPDATE Devis SET dateEmission = %s, dateValidite = %s, descriptionPrestation = %s, quantitePrevue = %s, detailsCouts = %s, montantTotalEstime = %s, statut = %s, dateAcceptation = %s, idClient = %s, numeroContrat = %s WHERE numeroDevis = %s"
        values = (devis.get_date_emission(), devis.get_date_validite(), devis.get_description_prestation(), devis.get_quantite_prevue(), devis.get_details_couts(
        ), devis.get_montant_total_estime(), devis.get_statut(), devis.get_date_acceptation(), devis.get_id_client(), devis.get_numero_contrat(), devis.get_numero_devis())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du Devis : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_devis(self, devis=None):
        les_devis = []
        sql = "SELECT * FROM Devis WHERE "

        if devis is None:
            sql = "SELECT * FROM Devis"
            values = []
        else:
            critere_numero_devis = devis.get_numero_devis()
            critere_date_emission = devis.get_date_emission()
            critere_date_validite = devis.get_date_validite()
            critere_description = devis.get_description_prestation()
            critere_quantite = devis.get_quantite_prevue()
            critere_details_couts = devis.get_details_couts()
            critere_montant = devis.get_montant_total_estime()
            critere_statut = devis.get_statut()
            critere_date_acceptation = devis.get_date_acceptation()
            critere_id_client = devis.get_id_client()
            critere_numero_contrat = devis.get_numero_contrat()

            values = []

            if critere_numero_devis is not None and critere_numero_devis != -1:
                sql += "numeroDevis = %s"
                values.append(critere_numero_devis)
            elif all(c is None for c in [critere_date_emission, critere_date_validite, critere_description, critere_quantite, critere_details_couts, critere_montant, critere_statut, critere_date_acceptation, critere_id_client, critere_numero_contrat]):
                sql = "SELECT * FROM Devis"
            else:
                conditions = []
                if critere_date_emission is not None:
                    conditions.append("dateEmission = %s")
                    values.append(critere_date_emission)
                if critere_date_validite is not None:
                    conditions.append("dateValidite = %s")
                    values.append(critere_date_validite)
                if critere_description is not None:
                    conditions.append("descriptionPrestation = %s")
                    values.append(critere_description)
                if critere_quantite is not None:
                    conditions.append("quantitePrevue = %s")
                    values.append(critere_quantite)
                if critere_details_couts is not None:
                    conditions.append("detailsCouts = %s")
                    values.append(critere_details_couts)
                if critere_montant is not None:
                    conditions.append("montantTotalEstime = %s")
                    values.append(critere_montant)
                if critere_statut is not None:
                    conditions.append("statut = %s")
                    values.append(critere_statut)
                if critere_date_acceptation is not None:
                    conditions.append("dateAcceptation = %s")
                    values.append(critere_date_acceptation)
                if critere_id_client is not None:
                    conditions.append("idClient = %s")
                    values.append(critere_id_client)
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
                les_devis.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de Devis : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_devis

    def set_all_values(self, rs):
        from domaine.Devis import Devis
        devis = Devis(rs["numeroDevis"], rs["dateEmission"], rs["dateValidite"], rs["descriptionPrestation"], rs["quantitePrevue"],
                      rs["detailsCouts"], rs["montantTotalEstime"], rs["statut"], rs["dateAcceptation"], rs["idClient"], rs["numeroContrat"])
        return devis
