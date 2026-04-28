from dao.DAODevis import DAODevis
from datetime import datetime

class Devis:

    leDAODevis = DAODevis.get_instance()

    def __init__(self, numero_devis: str = None, date_emission: str = None, date_validite: str = None, description_prestation: str = None, quantite_prevue: int = None, details_couts: str = None, montant_total_estime: float = None, statut: str = None, date_acceptation: str = None, id_client: int = None, numero_contrat: str = None):

        # verification Type :
        if not isinstance(numero_devis, str):
            raise TypeError(f"l'attribut {numero_devis} doit être une chaîne de caractere")
        
        if not isinstance(date_emission, str) and self.is_date(date_emission):
            raise TypeError(f"l'attribut {date_emission} doit être une chaîne de caractere")
        
        if not isinstance(date_validite, str) and self.is_date(date_validite):
            raise TypeError(f"l'attribut {date_validite} doit être une chaîne de caractères")
        
        if not isinstance(description_prestation, str):
            raise TypeError(f"l'attribut {description_prestation} doit être une chaîne de caractères")
        
        if not isinstance(quantite_prevue, int):
            raise TypeError(f"l'attribut {quantite_prevue} doit être un entier")
        
        if not isinstance(details_couts, str):
            raise TypeError(f"l'attribut {details_couts} doit être une chaîne de caractères ")
        
        if not isinstance(montant_total_estime, float):
            raise TypeError(f"l'attribut {montant_total_estime} doit être un float")
        
        if not isinstance(statut, str):
            raise TypeError(f"l'attribut {statut} doit être une chaîne de caractères")
        
        if date_acceptation is not None and not isinstance(date_acceptation, str) and self.is_date(date_acceptation):
            raise TypeError(f"l'attribut {date_acceptation} doit être une chaîne de caractères")
        
        if not isinstance(id_client, int):
            raise TypeError(f"l'attribut {id_client} doit être un entier")
        
        if numero_contrat is not None and not isinstance(numero_contrat, str):
            raise TypeError(f"l'attribut {numero_contrat} doit être une chaîne de caractères")

        self.__numero_devis = numero_devis
        self.__date_emission = date_emission
        self.__date_validite = date_validite
        self.__description_prestation = description_prestation
        self.__quantite_prevue = quantite_prevue
        self.__details_couts = details_couts
        self.__montant_total_estime = montant_total_estime
        self.__statut = statut
        self.__date_acceptation = date_acceptation
        self.__id_client = id_client
        self.__numero_contrat = numero_contrat

        self.__numero_devis = Devis.leDAODevis.insert_devis(self)

    #method statiques : 

    @staticmethod
    def charger(numero_devis):
        pass

    @staticmethod
    def supprimer(un_devis):
        pass

    # Getters

    def get_numero_devis(self):
        return self.__numero_devis

    def get_date_emission(self):
        return self.__date_emission

    def get_date_validite(self):
        return self.__date_validite

    def get_description_prestation(self):
        return self.__description_prestation

    def get_quantite_prevue(self):
        return self.__quantite_prevue

    def get_details_couts(self):
        return self.__details_couts

    def get_montant_total_estime(self):
        return self.__montant_total_estime

    def get_statut(self):
        return self.__statut

    def get_date_acceptation(self):
        return self.__date_acceptation

    def get_id_client(self):
        return self.__id_client

    def get_numero_contrat(self):
        return self.__numero_contrat

    # Setters

    def set_numero_devis(self, numero_devis):
        if not isinstance(numero_devis, str):
            raise TypeError(f"l'attribut {numero_devis} doit être une chaîne de caractere")
        
        self.__numero_devis = numero_devis
        Devis.leDAODevis.update_devis(self)

    def set_date_emission(self, date_emission):
        if not isinstance(date_emission, str) and self.is_date(date_emission):
            raise TypeError(f"l'attribut {date_emission} doit être une chaîne de caractere")
        
        self.__date_emission = date_emission
        Devis.leDAODevis.update_devis(self)

    def set_date_validite(self, date_validite):
        if not isinstance(date_validite, str) and self.is_date(date_validite):
            raise TypeError(f"l'attribut {date_validite} doit être une chaîne de caractères")
        
        self.__date_validite = date_validite
        Devis.leDAODevis.update_devis(self)

    def set_description_prestation(self, description_prestation):
        if not isinstance(description_prestation, str):
            raise TypeError(f"l'attribut {description_prestation} doit être une chaîne de caractères")
        
        self.__description_prestation = description_prestation
        Devis.leDAODevis.update_devis(self)

    def set_quantite_prevue(self, quantite_prevue):
        if not isinstance(quantite_prevue, int):
            raise TypeError(f"l'attribut {quantite_prevue} doit être un entier")
        self.__quantite_prevue = quantite_prevue
        Devis.leDAODevis.update_devis(self)

    def set_details_couts(self, details_couts):
        if not isinstance(details_couts, str):
            raise TypeError(f"l'attribut {details_couts} doit être une chaîne de caractères ")
        
        self.__details_couts = details_couts
        Devis.leDAODevis.update_devis(self)

    def set_montant_total_estime(self, montant_total_estime):
        if not isinstance(montant_total_estime, float):
            raise TypeError(f"l'attribut {montant_total_estime} doit être un float")
        
        self.__montant_total_estime = montant_total_estime
        Devis.leDAODevis.update_devis(self)

    def set_statut(self, statut):
        if not isinstance(statut, str):
            raise TypeError(f"l'attribut {statut} doit être une chaîne de caractères")
        
        self.__statut = statut
        Devis.leDAODevis.update_devis(self)

    def set_date_acceptation(self, date_acceptation):
        if not isinstance(date_acceptation, str) and self.is_date(date_acceptation):
            raise TypeError(f"l'attribut {date_acceptation} doit être une chaîne de caractères")
        
        self.__date_acceptation = date_acceptation
        Devis.leDAODevis.update_devis(self)

    def set_id_client(self, id_client):
        if not isinstance(id_client, int):
            raise TypeError(f"l'attribut {id_client} doit être un entier")
        
        self.__id_client = id_client
        Devis.leDAODevis.update_devis(self)

    def set_numero_contrat(self, numero_contrat):
        if not isinstance(numero_contrat, str):
            raise TypeError(f"l'attribut {numero_contrat} doit être une chaîne de caractères")
        
        self.__numero_contrat = numero_contrat
        Devis.leDAODevis.update_devis(self)

    def is_date(self, str_date : str) -> bool :
        format = "%Y-%m-%d"
        res = bool(datetime.strptime(str_date, format))
        if res is False : 
            raise ValueError(f"l'attributs doit être sous le format 'yyyy-mm-dd'")
        return res

    def __str__(self):
        return (f"Devis(numero_devis={self.__numero_devis}, date_emission={self.__date_emission}, date_validite={self.__date_validite}, description_prestation={self.__description_prestation}, quantite_prevue={self.__quantite_prevue}, details_couts={self.__details_couts}, montant_total_estime={self.__montant_total_estime}, statut={self.__statut}, date_acceptation={self.__date_acceptation}, id_client={self.__id_client}, numero_contrat={self.__numero_contrat})")


"""class Devis :

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

    
    def __str__(self):
        return f"Devis(id_devis={self.__id_devis}, description_prestation={self.__description_prestation}, quantite_photos_prevues={self.__quantite_photos_prevues}, quantite_videos_prevues={self.__quantite_videos_prevues}, details_couts={self.__details_couts}, montant_total={self.__montant_total}, date_emission={self.__date_emission}, date_validite={self.__date_validite}, statut={self.__enum_devis_statut}, id_client={self.__id_client})"""
