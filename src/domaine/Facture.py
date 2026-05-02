from dao.DAOFacture import DAOFacture
from dao.DAOPaiement import DAOPaiement
from datetime import datetime

from domaine.Paiement import Paiement

class Facture:

    leDAOFacture = DAOFacture.get_instance()
    leDAOPaiement = DAOPaiement.get_instance()

    def __init__(self, numero_facture: str = None, date_emission: str = None, montant_total: float = None, etat: str = None, numero_contrat: str = None):

        self.__date_emission = date_emission
        self.__montant_total = montant_total
        self.__etat = etat
        self.__numero_contrat = numero_contrat

        self.__les_paiements = []
        if numero_facture is not None : 
            self.__numero_facture = numero_facture
        else : 
            self.__numero_facture = Facture.leDAOFacture.insert_facture(self)

    #methode statiques : 

    @staticmethod
    def charger(numero_facture):
        un_facture = Facture.leDAOFacture.find_facture(numero_facture)
        un_paiement = Paiement(-1)
        un_paiement.set_numero_facture(numero_facture=numero_facture)
        un_facture.set_les_paiements(Facture.leDAOPaiement.select_paiement(un_paiement))
        return un_facture

    @staticmethod
    def supprimer(un_facture):
        if un_facture.get_les_paiements() : 
            raise Exception("Erreur_suppression_facture_avec_paiements")
        else :
            Facture.leDAOFacture.delete_facture(un_facture)
    
    def ajouter_paiement(self, paiement : Paiement ):
        if paiement.get_numero_facture() is None : 
            self.__les_paiements.append(paiement)
            paiement.set_numero_facture(self.__numero_facture)
        else : 
            raise Exception("Erreur_paiement_a_deja_un_contart")
    
    def enlever_paiement(self, paiment : Paiement):
        paiement2 = None
        for p in self.__les_paiements : 
            if p.get_numero_Facture() == paiment.get_numero_facture() :
                paiement2 = p
                break
        if paiement2 is not None : 
            self.__les_paiements.remove(paiement2)
            paiment.set_numero_facture(None)
        else : 
            raise Exception("Erreur_Paiement_inexistant_dans_les_paiements_du_facture")
        
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

    def get_les_paiements(self) : 
        return self.__les_paiements

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

    def set_les_paiements(self, les_paiements) :
        self.__les_paiements = les_paiements

    def is_date(self, str_date : str) -> bool :
        format = "%Y-%m-%d"
        res = bool(datetime.strptime(str_date, format))
        if res is False : 
            raise ValueError(f"l'attributs doit être sous le format 'yyyy-mm-dd'")
        return res

    def __str__(self):
        return f"Facture(numero_facture={self.__numero_facture}, date_emission={self.__date_emission}, montant_total={self.__montant_total}, etat={self.__etat}, numero_contrat={self.__numero_contrat})"

