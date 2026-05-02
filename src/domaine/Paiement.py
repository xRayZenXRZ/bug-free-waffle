from dao.DAOPaiement import DAOPAiement
from datetime import datetime

class Paiement:

    leDAOPaiement = DAOPAiement.get_instance()

    def __init__(self, id_paiement: int = None, date: str = None, montant: float = None, numero_Facture: str = None):

        self.__date = date
        self.__montant = montant
        self.__numero_Facture = numero_Facture

        if id_paiement is not None:
            self.__id_paiement = id_paiement
        else:
            self.__id_paiement = Paiement.leDAOPaiement.insert_paiement(self)

    # methode statiques : 

    @staticmethod
    def charger(id_paiement):
        return Paiement.leDAOPaiement.find_paiement(id_paiement)

    @staticmethod
    def supprimer(un_paiement):
        if un_paiement.get_numero_Facture() is None : 
            Paiement.leDAOPaiement.delete_paiement(un_paiement)
        else : 
            raise Exception("Erreur_suppression_paiement_avec_facture")
    
    # Getters

    def get_id_paiement(self):
        return self.__id_paiement

    def get_montant(self):
        return self.__montant

    def get_date(self):
        return self.__date

    def get_numero_facture(self):
        return self.__numero_Facture

    # Setters

    def set_id_paiement(self, id_paiement):
        if not isinstance(id_paiement, int):
            raise TypeError("l'attribut {id_paiement} doit être un entier")
        self.__id_paiement = id_paiement
        Paiement.leDAOPaiement.update_paiement(self)

    def set_date(self, date):
        if not isinstance(date, str) and self.is_date(date):
            raise TypeError(
                "l'attribut {date} doit être une chaîne de caractères")
        self.__date = date
        Paiement.leDAOPaiement.update_paiement(self)

    def set_montant(self, montant):
        if not isinstance(montant, float):
            raise TypeError("l'attribut {montant} doit être un nombre float")
        self.__montant = montant
        Paiement.leDAOPaiement.update_paiement(self)

    def set_numero_facture(self, numero_facture):
        if not isinstance(numero_facture, str):
            raise TypeError(
                "l'attribut {numero_Facture} doit être une chaîne de caractères")
        self.__numero_Facture = numero_facture
        Paiement.leDAOPaiement.update_paiement(self)

    def is_date(self, str_date : str) -> bool :
        format = "%Y-%m-%d"
        res = bool(datetime.strptime(str_date, format))
        if res is False : 
            raise ValueError(f"l'attributs doit être sous le format 'yyyy-mm-dd'")
        return res

    def __str__(self):
        return f"Paiement(id_paiement={self.__id_paiement}, date={self.__date}, montant={self.__montant}, numeroFacture={self.__numero_Facture})"
