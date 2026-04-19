from DAO.DAOActivite import DAOActivite

class Activite : 

    leDAOActivite = DAOActivite()

    def __init__(self, id_activite = None, libelle_operationnel = None, date_prevues = None, date_effective = None, duree_estimee = None, responsable =None , statut = None, id_prestation = None):

        self.__libelle_operationnel = libelle_operationnel
        self.__date_prevues = date_prevues
        self.__date_effective = date_effective
        self.__duree_estimee = duree_estimee
        self.__responsable = responsable
        self.__statut = statut
        self.__id_prestation = id_prestation

        if id_activite is not None : 
            self.__id_activite = id_activite
        else : 
            self.__id_activite = Activite.leDAOActivite.insert_activite(self)

    # Getters
    def get_id_activite(self):
        return self.__id_activite

    def get_libelle_operationnel(self):
        return self.__libelle_operationnel

    def get_date_prevues(self):
        return self.__date_prevues

    def get_date_effective(self):
        return self.__date_effective

    def get_duree_estimee(self):
        return self.__duree_estimee

    def get_responsable(self):
        return self.__responsable

    def get_statut(self):
        return self.__statut

    def get_id_prestation(self):
        return self.__id_prestation

    # Setters
    def set_id_activite(self, id_activite):
        self.__id_activite = id_activite

    def set_libelle_operationnel(self, libelle_operationnel):
        self.__libelle_operationnel = libelle_operationnel

    def set_date_prevues(self, date_prevues):
        self.__date_prevues = date_prevues

    def set_date_effective(self, date_effective):
        self.__date_effective = date_effective

    def set_duree_estimee(self, duree_estimee):
        self.__duree_estimee = duree_estimee

    def set_responsable(self, responsable):
        self.__responsable = responsable

    def set_statut(self, statut):
        self.__statut = statut

    def set_id_prestation(self, id_prestation):
        self.__id_prestation = id_prestation

    def __str__(self):
        return f"Activite(id_activite={self.__id_activite}, libelle_operationnel={self.__libelle_operationnel}, date_prevues={self.__date_prevues}, date_effective={self.__date_effective}, duree_estimee={self.__duree_estimee}, responsable={self.__responsable}, statut={self.__statut}, id_prestation={self.__id_prestation})"

"""class Activite : 

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

    def __str__(self):
        return f"Activite(id_activite={self.__id_activite}, activite={self.__enum_activite}, date_prevues={self.__date_prevues}, duree_estimee={self.__duree_estimee}, statut={self.__enum_activite_statut})"""