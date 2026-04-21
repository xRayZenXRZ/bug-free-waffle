from dao.DAOSession import DAOSession
from mysql.connector import Error


class DAOPrestation:

    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOPrestation.unique_instance is None:
            DAOPrestation.unique_instance = DAOPrestation()
        return DAOPrestation.unique_instance

    def insert_Prestation(self, prestation):
        sql = "INSERT INTO Prestation (datePrevue, dateEffective, lieu, type, nbPhotosPrevues, nbVideosPrevues, numeroContrat) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (prestation.get_date_prevue(), prestation.get_date_effective(), prestation.get_lieu(), prestation.get_type(
        ), prestation.get_nb_photos_prevues(), prestation.get_nb_videos_prevues(), prestation.get_numero_contrat())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la Prestation : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    def delete_prestation(self, prestation):
        sql = "DELETE FROM Prestation WHERE idPrestation = %s"
        values = (prestation.get_id_prestation(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la Prestation : {e}")
            print(sql)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_prestation(self, prestation):
        sql = "SELECT * FROM Prestation WHERE idPrestation = %s"
        values = (prestation.get_id_prestation(),)
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
            print(f"Erreur lors de la recherche d'une Prestation : {e}")
            print(sql)
            print(values)
            return None
        finally:
            if cursor:
                cursor.close()

    def update_prestation(self, prestation):
        sql = "UPDATE Prestation SET datePrevue = %s, dateEffective = %s, lieu = %s, type = %s, nbPhotosPrevues = %s, nbVideosPrevues = %s, numeroContrat = %s WHERE idPrestation = %s"
        values = (prestation.get_date_prevue(), prestation.get_date_effective(), prestation.get_lieu(), prestation.get_type(
        ), prestation.get_nb_photos_prevues(), prestation.get_nb_videos_prevues(), prestation.get_numero_contrat(), prestation.get_id_prestation())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la Prestation : {e}")
            print(sql)
            print(values)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def select_prestation(self, prestation=None):
        les_prestations = []
        sql = "SELECT * FROM Prestation WHERE "

        if prestation is None:
            sql = "SELECT * FROM Prestation"
            values = []
        else:
            critere_id_prestation = prestation.get_id_prestation()
            critere_date_prevue = prestation.get_date_prevue()
            critere_date_effective = prestation.get_date_effective()
            critere_lieu = prestation.get_lieu()
            critere_type = prestation.get_type()
            critere_nb_photos = prestation.get_nb_photos_prevues()
            critere_nb_videos = prestation.get_nb_videos_prevues()
            critere_numero_contrat = prestation.get_numero_contrat()

            values = []

            if critere_id_prestation is not None and critere_id_prestation != -1:
                sql += "idPrestation = %s"
                values.append(critere_id_prestation)
            elif all(c is None for c in [critere_date_prevue, critere_date_effective, critere_lieu, critere_type, critere_nb_photos, critere_nb_videos, critere_numero_contrat]):
                sql = "SELECT * FROM Prestation"
            else:
                conditions = []
                if critere_date_prevue is not None:
                    conditions.append("datePrevue = %s")
                    values.append(critere_date_prevue)
                if critere_date_effective is not None:
                    conditions.append("dateEffective = %s")
                    values.append(critere_date_effective)
                if critere_lieu is not None:
                    conditions.append("lieu = %s")
                    values.append(critere_lieu)
                if critere_type is not None:
                    conditions.append("type = %s")
                    values.append(critere_type)
                if critere_nb_photos is not None:
                    conditions.append("nbPhotosPrevues = %s")
                    values.append(critere_nb_photos)
                if critere_nb_videos is not None:
                    conditions.append("nbVideosPrevues = %s")
                    values.append(critere_nb_videos)
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
                les_prestations.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de Prestations : {e}")
            print(sql)
            print(values)
        finally:
            if cursor:
                cursor.close()
        return les_prestations

    def set_all_values(self, rs):
        from domaine.Prestation import Prestation
        prestation = Prestation(rs["idPrestation"], rs["datePrevue"], rs["dateEffective"], rs["lieu"],
                                rs["type"], rs["nbPhotosPrevues"], rs["nbVideosPrevues"], rs["numeroContrat"])
        return prestation
