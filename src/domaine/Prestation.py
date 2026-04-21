from dao.DAOPrestation import DAOPrestation

class Prestation:

    leDAOPrestation = DAOPrestation.get_instance()

    def __init__(self, id_prestation : int = None, date_prevue : str = None, date_effective : str = None, lieu : str =None, type_prestation : str =None, nb_photos_prevues : int =None, nb_videos_prevues : int =None, numero_contrat : str =None):
        
        #verification type : 
        if id_prestation is not None and not isinstance(id_prestation, int):
            raise TypeError("l'attribut {id_prestation} doit être un entier")
        if date_prevue is not None and not isinstance(date_prevue, str):
            raise TypeError("l'attribut {date_prevue} doit être une chaîne de caractères")
        if date_effective is not None and not isinstance(date_effective, str):
            raise TypeError("l'attribut {date_effective} doit être une chaîne de caractères")
        if lieu is not None and not isinstance(lieu, str):
            raise TypeError("l'attribut {lieu} doit être une chaîne de caractères")
        if type_prestation is not None and not isinstance(type_prestation, str):
            raise TypeError("l'attribut {type_prestation} doit être une chaîne de caractères")
        if nb_photos_prevues is not None and not isinstance(nb_photos_prevues, int):
            raise TypeError("l'attribut {nb_photos_prevues} doit être un entier")
        if nb_videos_prevues is not None and not isinstance(nb_videos_prevues, int):
            raise TypeError("l'attribut {nb_videos_prevues} doit être un entier")
        if numero_contrat is not None and not isinstance(numero_contrat, str):
            raise TypeError("l'attribut {numero_contrat} doit être une chaîne de caractères")

        # Vérification des valeurs numériques positives -> à refaire sur les autres classes...
        if nb_photos_prevues is not None and nb_photos_prevues < 0:
            raise ValueError("le nombre de photos prévues ne peut pas être négatif")
        if nb_videos_prevues is not None and nb_videos_prevues < 0:
            raise ValueError("le nombre de vidéos prévues ne peut pas être négatif")

        self.__date_prevue = date_prevue
        self.__date_effective = date_effective
        self.__lieu = lieu
        self.__type = type_prestation
        self.__nb_photos_prevues = nb_photos_prevues
        self.__nb_videos_prevues = nb_videos_prevues
        self.__numero_contrat = numero_contrat

        if id_prestation is not None:
            self.__id_prestation = id_prestation
        else:
            self.__id_prestation = Prestation.leDAOPrestation.insert_Prestation(self)

    # Getters

    def get_id_prestation(self):
        return self.__id_prestation

    def get_date_prevue(self):
        return self.__date_prevue

    def get_date_effective(self):
        return self.__date_effective

    def get_lieu(self):
        return self.__lieu

    def get_type(self):
        return self.__type

    def get_nb_photos_prevues(self):
        return self.__nb_photos_prevues

    def get_nb_videos_prevues(self):
        return self.__nb_videos_prevues

    def get_numero_contrat(self):
        return self.__numero_contrat

    # Setters

    def set_id_prestation(self, id_prestation):
        if not isinstance(id_prestation, int):
            raise TypeError("l'attribut {id_prestation} doit être un entier")
        self.__id_prestation = id_prestation
        Prestation.leDAOPrestation.update_prestation(self)

    def set_date_prevue(self, date_prevue):
        if date_prevue is not None and not isinstance(date_prevue, str):
            raise TypeError("l'attribut {date_prevue} doit être une chaîne de caractères ou None")
        self.__date_prevue = date_prevue
        Prestation.leDAOPrestation.update_prestation(self)

    def set_date_effective(self, date_effective):
        if date_effective is not None and not isinstance(date_effective, str):
            raise TypeError("l'attribut {date_effective} doit être une chaîne de caractères ou None")
        self.__date_effective = date_effective
        Prestation.leDAOPrestation.update_prestation(self)

    def set_lieu(self, lieu):
        if lieu is not None and not isinstance(lieu, str):
            raise TypeError("l'attribut {lieu} doit être une chaîne de caractères ou None")
        self.__lieu = lieu
        Prestation.leDAOPrestation.update_prestation(self)

    def set_type(self, type_prestation):
        if type_prestation is not None and not isinstance(type_prestation, str):
            raise TypeError("l'attribut {type_prestation} doit être une chaîne de caractères ou None")
        self.__type = type_prestation
        Prestation.leDAOPrestation.update_prestation(self)

    def set_nb_photos_prevues(self, nb_photos_prevues):
        if not isinstance(nb_photos_prevues, int):
            raise TypeError("l'attribut {nb_photos_prevues} doit être un entier")
        if nb_photos_prevues < 0:
            raise ValueError("le nombre de photos prévues ne peut pas être négatif")
        self.__nb_photos_prevues = nb_photos_prevues
        Prestation.leDAOPrestation.update_prestation(self)

    def set_nb_videos_prevues(self, nb_videos_prevues):
        if not isinstance(nb_videos_prevues, int):
            raise TypeError("l'attribut {nb_videos_prevues} doit être un entier")
        if nb_videos_prevues < 0:
            raise ValueError("le nombre de vidéos prévues ne peut pas être négatif")
        self.__nb_videos_prevues = nb_videos_prevues
        Prestation.leDAOPrestation.update_prestation(self)

    def set_numero_contrat(self, numero_contrat):
        if numero_contrat is not None and not isinstance(numero_contrat, str):
            raise TypeError("l'attribut {numero_contrat} doit être une chaîne de caractères ou None")
        self.__numero_contrat = numero_contrat
        Prestation.leDAOPrestation.update_prestation(self)

    def __str__(self):
        return f"Prestation(id_prestation={self.__id_prestation}, date_prevue={self.__date_prevue}, date_effective={self.__date_effective}, lieu={self.__lieu}, type={self.__type}, nb_photos_prevues={self.__nb_photos_prevues}, nb_videos_prevues={self.__nb_videos_prevues}, numero_contrat={self.__numero_contrat})"
    
"""class Prestation : 

    def __init__(self, id_prestation, date_prevues, date_effective, lieu, quantite_photos_prevues, quantite_videos_prevues, enum_prestation_type, enum_prestation_mission):
        self.__id_prestation = id_prestation
        self.__date_prevues = date_prevues
        self.__date_effective = date_effective
        self.__lieu = lieu
        self.__quantite_photos_prevues = quantite_photos_prevues
        self.__quantite_videos_prevues = quantite_videos_prevues
        self.__enum_prestation_type = enum_prestation_type
        self.__enum_prestation_mission = enum_prestation_mission

    # Getters
    def get_id_prestation(self):
        return self.__id_prestation

    def get_date_prevues(self):
        return self.__date_prevues

    def get_date_effective(self):
        return self.__date_effective

    def get_lieu(self):
        return self.__lieu

    def get_quantite_photos_prevues(self):
        return self.__quantite_photos_prevues

    def get_quantite_videos_prevues(self):
        return self.__quantite_videos_prevues

    def get_enum_prestation_type(self):
        return self.__enum_prestation_type

    def get_enum_prestation_mission(self):
        return self.__enum_prestation_mission

    # Setters

    # Commentaire : verification à faire plus tard...

    def set_id_prestation(self, id_prestation):
        self.__id_prestation = id_prestation

    def set_date_prevues(self, date_prevues):
        self.__date_prevues = date_prevues

    def set_date_effective(self, date_effective):
        self.__date_effective = date_effective

    def set_lieu(self, lieu):
        self.__lieu = lieu

    def set_quantite_photos_prevues(self, quantite_photos_prevues):
        self.__quantite_photos_prevues = quantite_photos_prevues

    def set_quantite_videos_prevues(self, quantite_videos_prevues):
        self.__quantite_videos_prevues = quantite_videos_prevues

    def set_enum_prestation_type(self, enum_prestation_type):
        self.__enum_prestation_type = enum_prestation_type

    def set_enum_prestation_mission(self, enum_prestation_mission):
        self.__enum_prestation_mission = enum_prestation_mission
    
    def __str__(self):
        return f"Prestation(date_prevues={self.__date_prevues}, date_effective={self.__date_effective}, lieu={self.__lieu}, quantite_photos_prevues={self.__quantite_photos_prevues}, quantite_videos_prevues={self.__quantite_videos_prevues}, type_prestation={self.__enum_prestation_type}, mission={self.__enum_prestation_mission})"""