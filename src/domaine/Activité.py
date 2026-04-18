class Activite : 

    def __init__(self, id_activite, enum_activite, date_prevues, duree_estimee, enum_activite_statut):
        self.__id_activite = id_activite
        self.__enum_activite = enum_activite
        self.__date_prevues = date_prevues
        self.__duree_estimee = duree_estimee
        self.__enum_activite_statut = enum_activite_statut

    #EnumEmployeeStatus pas déclarer car attente rep prof

    # Getters
    def get_id_activite(self):
        return self.__id_activite

    def get_enum_activite(self):
        return self.__enum_activite

    def get_date_prevues(self):
        return self.__date_prevues

    def get_duree_estimee(self):
        return self.__duree_estimee

    def get_enum_activite_statut(self):
        return self.__enum_activite_statut

    # Setters

    #Commentaire : verification à faire ....

    def set_id_activite(self, id_activite):
        self.__id_activite = id_activite

    def set_enum_activite(self, enum_activite):
        self.__enum_activite = enum_activite

    def set_date_prevues(self, date_prevues):
        self.__date_prevues = date_prevues

    def set_duree_estimee(self, duree_estimee):
        self.__duree_estimee = duree_estimee

    def set_enum_activite_statut(self, enum_activite_statut):
        self.__enum_activite_statut = enum_activite_statut