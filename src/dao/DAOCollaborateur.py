from dao.DAOSession import DAOSession

class DAOCollaborateur:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOCollaborateur.unique_instance is None:
            DAOCollaborateur.unique_instance = DAOCollaborateur()
        return DAOCollaborateur.unique_instance

    @staticmethod
    def creer_collaborateur(id_utilisateur, poste, telephone_pro):
        """Crée un collaborateur lié à un utilisateur existant"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor()
            query = """
                INSERT INTO Collaborateur (idUtilisateur, poste, telephonePro)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (id_utilisateur, poste, telephone_pro))
            conn.commit()
            id_genere = cursor.lastrowid
            cursor.close()
            return (True, id_genere)
        except Exception as e:
            print(f"Erreur lors de la création du collaborateur : {e}")
            return (False, str(e))

    @staticmethod
    def update_collaborateur(collaborateur):
        """Met à jour les informations spécifiques au collaborateur"""
        try:
            conn = DAOSession.get_connexion()
            cursor = conn.cursor()
            query = """
                UPDATE Collaborateur 
                SET poste = %s, telephonePro = %s 
                WHERE idCollaborateur = %s
            """
            cursor.execute(query, (
                collaborateur.get_poste(),
                collaborateur.get_telephone_pro(),
                collaborateur.get_id_collaborateur()
            ))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour du collaborateur : {e}")
            return False
