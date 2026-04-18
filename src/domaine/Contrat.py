class Contrat :

    def __init__(self, id_contrat, duree, nb_photos_publication_prevues, nb_videos_publication_prevues, montat_global, enum_contrat_periodicite_publication_prevues, enum_prestation, enum_paiements_conditions, enum_contrat_prestation_type, id_devis = None ):
        self.__id_contrat = id_contrat
        self.__duree = duree
        self.__nb_photos_publication_prevues = nb_photos_publication_prevues
        self.__nb_videos_publication_prevues = nb_videos_publication_prevues
        self.__montat_global = montat_global
        self.__enum_contrat_periodicite_publication_prevues = enum_contrat_periodicite_publication_prevues
        self.__enum_prestation = enum_prestation
        self.__enum_paiements_conditions = enum_paiements_conditions
        self.__enum_contrat_prestation_type = enum_contrat_prestation_type

        #Foreign Key :
        self.__id_devis = id_devis

    # Getters
    def get_id_contrat(self):
        return self.__id_contrat

    def get_duree(self):
        return self.__duree

    def get_nb_photos_publication_prevues(self):
        return self.__nb_photos_publication_prevues

    def get_nb_videos_publication_prevues(self):
        return self.__nb_videos_publication_prevues

    def get_montat_global(self):
        return self.__montat_global

    def get_enum_contrat_periodicite_publication_prevues(self):
        return self.__enum_contrat_periodicite_publication_prevues

    def get_enum_prestation(self):
        return self.__enum_prestation

    def get_enum_paiements_conditions(self):
        return self.__enum_paiements_conditions

    def get_enum_contrat_prestation_type(self):
        return self.__enum_contrat_prestation_type

    def get_id_devis(self):
        return self.__id_devis

    # Setters

    #Commentaire : Verification à faire...

    def set_id_contrat(self, id_contrat):
        self.__id_contrat = id_contrat

    def set_duree(self, duree):
        self.__duree = duree

    def set_nb_photos_publication_prevues(self, nb_photos_publication_prevues):
        self.__nb_photos_publication_prevues = nb_photos_publication_prevues

    def set_nb_videos_publication_prevues(self, nb_videos_publication_prevues):
        self.__nb_videos_publication_prevues = nb_videos_publication_prevues

    def set_montat_global(self, montat_global):
        self.__montat_global = montat_global

    def set_enum_contrat_periodicite_publication_prevues(self, enum_contrat_periodicite_publication_prevues):
        self.__enum_contrat_periodicite_publication_prevues = enum_contrat_periodicite_publication_prevues

    def set_enum_prestation(self, enum_prestation):
        self.__enum_prestation = enum_prestation

    def set_enum_paiements_conditions(self, enum_paiements_conditions):
        self.__enum_paiements_conditions = enum_paiements_conditions

    def set_enum_contrat_prestation_type(self, enum_contrat_prestation_type):
        self.__enum_contrat_prestation_type = enum_contrat_prestation_type

    def set_id_devis(self, id_devis):
        self.__id_devis = id_devis

    def __str__(self):
        return f"Contrat(id_contrat={self.__id_contrat}, duree={self.__duree}, nb_photos_publication_prevues={self.__nb_photos_publication_prevues}, nb_videos_publication_prevues={self.__nb_videos_publication_prevues}, montat_global={self.__montat_global}, periodicite_publication={self.__enum_contrat_periodicite_publication_prevues}, prestation={self.__enum_prestation}, conditions_paiements={self.__enum_paiements_conditions}, type_prestation={self.__enum_contrat_prestation_type}, id_devis={self.__id_devis})"