from dao.DAOContrat import DAOContrat
from dao.DAOClient import DAOClient
<<<<<<< HEAD
from dao.DAODevis import DAODevis
from dao.DAOFacture import DAOFacture
from dao.DAOPrestation import DAOPrestation
from domaine.Prestation import Prestation
=======
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357
from domaine.Client import Client
from domaine.Devis import Devis
from domaine.Facture import Facture

from datetime import datetime



class Contrat:

    leDAOContrat = DAOContrat.get_instance()
    leDAODevis = DAODevis.get_instance()
    leDAOFacture = DAOFacture.get_instance()
    leDAOPrestation = DAOPrestation.get_instance()

    def __init__(self, numero_contrat: str = None, date_debut: str = None, duree: str = None, nb_productions_totales: int = None, periodicite: str = None, montant_global: float = None, condition_paiements: str = None, id_client: int = None):

        self.__date_debut = date_debut
        self.__duree = duree
        self.__nb_productions_totales = nb_productions_totales
        self.__periodicite = periodicite
        self.__montant_global = montant_global
        self.__condition_paiements = condition_paiements
        self.__id_client = id_client

        self.__les_devis = [] 
        self.__les_factures = [] 
        self.__les_prestations = [] 
        #self.__les_clients = [] # --> faire les getters et les setters (à faire après avoir fais liens clients --> contrats)

        if numero_contrat is not None :
            self.__numero_contrat = numero_contrat
        else :
            self.__numero_contrat = Contrat.leDAOContrat.insert_contrat(self)

    #Method statiques : 

    @staticmethod
    def charger(numero_contrat):
        un_contrat = Contrat.leDAOContrat.find_contrat(numero_contrat)
        un_devis = Devis("-1")
        une_facture = Facture("-1")
        une_prestation = Prestation(-1)

        un_devis.set_numero_contrat(numero_contrat=numero_contrat)
        une_facture.set_numero_contrat(numero_contrat=numero_contrat)
        une_prestation.set_numero_contrat(numero_contrat=numero_contrat)
        
        un_contrat.set_les_devis(Contrat.leDAODevis.select_devis(un_devis))
        un_contrat.set_les_factures(Contrat.leDAOFacture.select_facture(une_facture))
        un_contrat.set_les_prestations(Contrat.leDAOPrestation.select_prestation(une_prestation))
        return un_contrat

    @staticmethod
    def supprimer(un_contrat):
        if un_contrat.get_les_devis() and un_contrat.get_les_factures() and un_contrat.get_les_prestations() : 
            raise Exception("Erreur_suppression_contrat_avec_devis_factures_prestations")
        else : 
            Contrat.leDAOContrat.delete_contrat(un_contrat)

    def ajouter_devis(self, devis : Devis) :
        if devis.get_numero_contrat() is None :
            self.__les_devis.append(devis)
            devis.set_numero_contrat(self.__numero_contrat)
        else : 
            raise Exception("Erreur_devis_a_deja_un_contrat")

    def ajouter_facture(self, facture : Facture) :
        if facture.get_numero_contrat() is None :
            self.__les_factures.append(facture)
            facture.set_numero_contrat(self.__numero_contrat)
        else : 
            raise Exception("Erreur_facture_a_deja_un_contrat")

    def ajouter_prestation(self, prestation : Prestation) :
        if prestation.get_numero_contrat() is None :
            self.__les_prestations.append(prestation)
            prestation.set_numero_contrat(self.__numero_contrat)
        else : 
            raise Exception("Erreur_prestation_a_deja_un_contrat")
    
    def enlever_devis(self, devis : Devis):
        devis2 = None
        for d in self.__les_devis : 
            if d.get_numero_devis() == devis.get_numero_contrat():
                devis2 = d
                break
        if devis2 is not None : 
            self.__les_devis.remove(devis2)
            devis.set_numero_contrat(None)
        else : 
            raise Exception("Erreur_Devis_inexistant_dans_les_devis_du_contrat")
        
    def enlever_prestation(self, prestation: Prestation):
        prestation2 = None
        for p in self.__les_prestations:
            if p.get_numero_prestation() == prestation.get_numero_prestation():
                prestation2 = p
                break
        if prestation2 is not None:
            self.__les_prestations.remove(prestation2)
            prestation.set_numero_prestation(None)
        else:
            raise Exception("Erreur_Prestation_inexistante_dans_les_prestations_du_contrat")

    def enlever_facture(self, facture: Facture):
        facture2 = None
        for f in self.__les_factures:
            if f.get_numero_facture() == facture.get_numero_facture():
                facture2 = f
                break
        if facture2 is not None:
            self.__les_factures.remove(facture2)
            facture.set_numero_facture(None)  # Si applicable
        else:
            raise Exception("Erreur_Facture_inexistante_dans_les_factures_du_contrat") 
    
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
    
    def get_les_devis(self):
        return self.__les_devis
    
    def get_les_factures(self):
        return self.__les_factures
    
    def get_les_prestations(self) : 
        return self.__les_prestations

    def get_id_client(self):
        return self.__id_client

    # Setters

    def set_numero_contrat(self, numero_contrat):
        if not isinstance(numero_contrat, str):
            raise TypeError(f"l'attribut {numero_contrat} doit être une chaine de caractère")
        
        self.__numero_contrat = numero_contrat
        Contrat.leDAOContrat.update_contrat(self)

    def set_date_debut(self, date_debut):
        if not isinstance(date_debut, str) and self.is_date(date_debut):
            raise TypeError(f"l'attribut {date_debut} doit être une chaine de caractère")
        
        self.__date_debut = date_debut
        Contrat.leDAOContrat.update_contrat(self)

    def set_duree(self, duree):
        if not isinstance(duree, str):
            raise TypeError(f"l'attribut {duree} doit être une chaine de caractère")
        
        self.__duree = duree
        Contrat.leDAOContrat.update_contrat(self)

    def set_nb_productions_totales(self, nb_productions_totales):
        if not isinstance(nb_productions_totales, int):
            raise TypeError(f"l'attribut {nb_productions_totales} doit être un entier")
        
        self.__nb_productions_totales = nb_productions_totales
        Contrat.leDAOContrat.update_contrat(self)

    def set_periodicite(self, periodicite):
        if not isinstance(periodicite, str):
            raise TypeError(f"l'attribut {periodicite} doit être une chaine de caractère")
        
        self.__periodicite = periodicite
        Contrat.leDAOContrat.update_contrat(self)

    def set_montant_global(self, montant_global):
        if not isinstance(montant_global, float):
            raise TypeError(f"l'attribut {montant_global} doit être un float")
        
        self.__montant_global = montant_global
        Contrat.leDAOContrat.update_contrat(self)

    def set_condition_paiements(self, condition_paiements):
        if not isinstance(condition_paiements, str):
            raise TypeError(f"l'attribut {condition_paiements} doit être une chaine de caractère")
        
        self.__condition_paiements = condition_paiements
        Contrat.leDAOContrat.update_contrat(self)

    def set_id_client(self, id_client):
        if not isinstance(id_client, int):
            raise TypeError(f"l'attribut {id_client} doit être une chaine de caractère")
        
        self.__id_client = id_client
        Contrat.leDAOContrat.update_contrat(self)

    def set_les_devis(self, les_devis) :
        self.__les_devis = les_devis

    def set_les_factures(self, les_factures) : 
        self.__les_factures = les_factures

    def set_les_prestations(self, les_prestations) :
        self.__les_prestations = les_prestations


    def is_date(self, str_date : str) -> bool :
        format = "%Y-%m-%d"
        res = bool(datetime.strptime(str_date, format))
        if res is False : 
            raise ValueError(f"l'attributs doit être sous le format 'yyyy-mm-dd'")
        return res

    def __str__(self):
        return (f"Contrat(numero_contrat={self.__numero_contrat}, date_debut={self.__date_debut}, duree={self.__duree}, nb_productions_totales={self.__nb_productions_totales}, periodicite={self.__periodicite}, montant_global={self.__montant_global}, condition_paiements={self.__condition_paiements}, id_client={self.__id_client})")