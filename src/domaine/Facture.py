from dao.DAOFacture import DAOFacture
from datetime import datetime

class Facture:

    leDAOFacture = DAOFacture.get_instance()

    def __init__(self, numero_facture: str = None, date_emission: str = None, montant_total: float = None, etat: str = None, numero_contrat: str = None):

        # verification type :
        if not isinstance(numero_facture, str):
            raise TypeError(f"l'attribut {numero_facture} doit être une chaîne de caractères")
        
        if not isinstance(date_emission, str) and self.is_date(date_emission):
            raise TypeError(f"l'attribut {date_emission} doit être une chaîne de caractères")
        
        if not isinstance(montant_total, float):
            raise TypeError(f"l'attribut {montant_total} doit être un nombre float")
        
        if not isinstance(etat, str):
            raise TypeError(f"l'attribut {etat} doit être une chaîne de caractères")
        
        if not isinstance(numero_contrat, str):
            raise TypeError(f"l'attribut {numero_contrat} doit être une chaîne de caractères")

        self.__numero_facture = numero_facture
        self.__date_emission = date_emission
        self.__montant_total = montant_total
        self.__etat = etat
        self.__numero_contrat = numero_contrat

        self.__numero_facture = Facture.leDAOFacture.insert_facture(self)

    # Getters

    def get_numero_facture(self):
        return self.__numero_facture

    def get_date_emission(self):
        return self.__date_emission

    def get_montant_total(self):
        return self.__montant_total

    def get_etat(self):
        return self.__etat

    def get_numero_contrat(self):
        return self.__numero_contrat

    # Setters

    def set_numero_facture(self, numero_facture):
        if not isinstance(numero_facture, str):
            raise TypeError(
                "l'attribut {numero_facture} doit être une chaîne de caractères")
        self.__numero_facture = numero_facture
        Facture.leDAOFacture.update_facture(self)

    def set_date_emission(self, date_emission) :
        if not isinstance(date_emission, str) and self.is_date(date_emission):
            raise TypeError(
                "l'attribut {date_emission} doit être une chaîne de caractères")
        self.__date_emission = date_emission
        Facture.leDAOFacture.update_facture(self)

    def set_montant_total(self, montant_total):
        if not isinstance(montant_total, float):
            raise TypeError(
                "l'attribut {montant_total} doit être un nombre float")
        self.__montant_total = montant_total
        Facture.leDAOFacture.update_facture(self)

    def set_etat(self, etat):
        if not isinstance(etat, str):
            raise TypeError(
                "l'attribut {etat} doit être une chaîne de caractères")
        self.__etat = etat
        Facture.leDAOFacture.update_facture(self)

    def set_numero_contrat(self, numero_contrat):
        if not isinstance(numero_contrat, str):
            raise TypeError(
                "l'attribut {numero_contrat} doit être une chaîne de caractères")
        self.__numero_contrat = numero_contrat
        Facture.leDAOFacture.update_facture(self)

    def is_date(self, str_date : str) -> bool :
        format = "%Y-%m-%d"
        res = bool(datetime.strptime(str_date, format))
        if res is False : 
            raise ValueError(f"l'attributs doit être sous le format 'yyyy-mm-dd'")
        return res

    def __str__(self):
        return f"Facture(numero_facture={self.__numero_facture}, date_emission={self.__date_emission}, montant_total={self.__montant_total}, etat={self.__etat}, numero_contrat={self.__numero_contrat})"


"""class Facture : 

    def __init__(self, id_facture, num_facture, date_emission, montant_total, enum_facture_etat):
        self.__id_facture = id_facture
        self.__num_facture = num_facture
        self.__date_emission = date_emission
        self.__montant_total = montant_total
        self.__enum_facture_etat = enum_facture_etat

    # Getters
    def get_id_facture(self):
        return self.__id_facture

    def get_num_facture(self):
        return self.__num_facture

    def get_date_emission(self):
        return self.__date_emission

    def get_montant_total(self):
        return self.__montant_total

    def get_enum_facture_etat(self):
        return self.__enum_facture_etat

    # Setters

    #Commentaire : yeahhh same things todo...

    def set_id_facture(self, id_facture):
        self.__id_facture = id_facture

    def set_num_facture(self, num_facture):
        self.__num_facture = num_facture

    def set_date_emission(self, date_emission):
        self.__date_emission = date_emission

    def set_montant_total(self, montant_total):
        self.__montant_total = montant_total

    def set_enum_facture_etat(self, enum_facture_etat):
        self.__enum_facture_etat = enum_facture_etat
    
    def __str__(self):
        return f"Facture(id_facture={self.__id_facture}, num_facture={self.__num_facture}, date_emission={self.__date_emission}, montant_total={self.__montant_total}, etat={self.__enum_facture_etat})"""
