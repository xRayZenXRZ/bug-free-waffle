
class Devis :

    def __init__(self, id_devis, description_prestation, quantite_photos_prevues, quantite_videos_prevues, details_couts, montant_total, date_emission, date_validite, enum_devis_statut, id_client = None):
        
        self.__id_devis = id_devis
        self.__description_prestation = description_prestation
        self.__quantite_photos_prevues = quantite_photos_prevues
        self.__quantite_videos_prevues = quantite_videos_prevues
        self.__details_couts = details_couts
        self.__montant_total = montant_total
        self.__date_emission = date_emission
        self.__date_validite = date_validite
        self.__enum_devis_statut = enum_devis_statut

        #Foreign Key :
        self.__id_client : int = id_client

    # Getters
    def get_id_devis(self):
        return self.__id_devis

    def get_description_prestation(self):
        return self.__description_prestation

    def get_quantite_photos_prevues(self):
        return self.__quantite_photos_prevues

    def get_quantite_videos_prevues(self):
        return self.__quantite_videos_prevues

    def get_details_couts(self):
        return self.__details_couts

    def get_montant_total(self):
        return self.__montant_total

    def get_date_emission(self):
        return self.__date_emission

    def get_date_validite(self):
        return self.__date_validite

    def get_enum_devis_statut(self):
        return self.__enum_devis_statut

    def get_id_client(self):
        return self.__id_client

    # Setters 

    # Commentaire : faire les verifications...

    def set_id_devis(self, id_devis):
        self.__id_devis = id_devis

    def set_description_prestation(self, description_prestation):
        self.__description_prestation = description_prestation

    def set_quantite_photos_prevues(self, quantite_photos_prevues):
        self.__quantite_photos_prevues = quantite_photos_prevues

    def set_quantite_videos_prevues(self, quantite_videos_prevues):
        self.__quantite_videos_prevues = quantite_videos_prevues

    def set_details_couts(self, details_couts):
        self.__details_couts = details_couts

    def set_montant_total(self, montant_total):
        self.__montant_total = montant_total

    def set_date_emission(self, date_emission):
        self.__date_emission = date_emission

    def set_date_validite(self, date_validite):
        self.__date_validite = date_validite

    def set_enum_devis_statut(self, enum_devis_statut):
        self.__enum_devis_statut = enum_devis_statut

    def set_id_client(self, id_client):
        self.__id_client = id_client

    
