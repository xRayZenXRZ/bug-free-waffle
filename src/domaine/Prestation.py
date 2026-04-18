class Prestation : 

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
        return f"Prestation(date_prevues={self.__date_prevues}, date_effective={self.__date_effective}, lieu={self.__lieu}, quantite_photos_prevues={self.__quantite_photos_prevues}, quantite_videos_prevues={self.__quantite_videos_prevues}, type_prestation={self.__enum_prestation_type}, mission={self.__enum_prestation_mission})"