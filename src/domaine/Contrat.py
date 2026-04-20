from DAO.DAOContrat import DAOContrat
from DAO.DAOClient import DAOClient
from domaine.Client import Client

class Contrat:

    leDAOContrat = DAOContrat.get_instance()

    def __init__(self, numero_contrat : str =None, date_debut : str =None, duree : int =None, nb_productions_totales : int =None, periodicite : str = None, montant_global : float =None, condition_paiements : str=None, id_client : int =None):

        self.__numero_contrat = numero_contrat
        self.__date_debut = date_debut
        self.__duree = duree
        self.__nb_productions_totales = nb_productions_totales
        self.__periodicite = periodicite
        self.__montant_global = montant_global
        self.__condition_paiements = condition_paiements
        self.__id_client = id_client

        self.__numero_contrat = Contrat.leDAOContrat.insert_contrat(self)

    # Getters

    def get_numero_contrat(self):
        return self.__numero_contrat

    def get_date_debut(self):
        return self.__date_debut

    def get_duree(self):
        return self.__duree

    def get_nb_productions_totales(self):
        return self.__nb_productions_totales

    def get_periodicite(self):
        return self.__periodicite

    def get_montant_global(self):
        return self.__montant_global

    def get_condition_paiements(self):
        return self.__condition_paiements

    def get_id_client(self):
        return self.__id_client

    # Setters

    def set_numero_contrat(self, numero_contrat):
        self.__numero_contrat = numero_contrat

    def set_date_debut(self, date_debut):
        self.__date_debut = date_debut
        Contrat.leDAOContrat.update_contrat(self)

    def set_duree(self, duree):
        self.__duree = duree
        Contrat.leDAOContrat.update_contrat(self)

    def set_nb_productions_totales(self, nb_productions_totales):
        self.__nb_productions_totales = nb_productions_totales
        Contrat.leDAOContrat.update_contrat(self)

    def set_periodicite(self, periodicite):
        self.__periodicite = periodicite
        Contrat.leDAOContrat.update_contrat(self)

    def set_montant_global(self, montant_global):
        self.__montant_global = montant_global
        Contrat.leDAOContrat.update_contrat(self)

    def set_condition_paiements(self, condition_paiements):
        self.__condition_paiements = condition_paiements
        Contrat.leDAOContrat.update_contrat(self)

    def set_id_client(self, id_client):
        self.__id_client = id_client
        Contrat.leDAOContrat.update_contrat(self)

    def __str__(self):
        return (f"Contrat(numero_contrat={self.__numero_contrat}, date_debut={self.__date_debut}, duree={self.__duree}, nb_productions_totales={self.__nb_productions_totales}, periodicite={self.__periodicite}, montant_global={self.__montant_global}, condition_paiements={self.__condition_paiements}, id_client={self.__id_client})")

"""class Contrat :

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
        return f"Contrat(id_contrat={self.__id_contrat}, duree={self.__duree}, nb_photos_publication_prevues={self.__nb_photos_publication_prevues}, nb_videos_publication_prevues={self.__nb_videos_publication_prevues}, montat_global={self.__montat_global}, periodicite_publication={self.__enum_contrat_periodicite_publication_prevues}, prestation={self.__enum_prestation}, conditions_paiements={self.__enum_paiements_conditions}, type_prestation={self.__enum_contrat_prestation_type}, id_devis={self.__id_devis})"""