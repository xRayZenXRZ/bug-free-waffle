from DAO.DAOFacture import DAOFacture

class Facture : 

    leDAOFacture = DAOFacture()

    def __init__(self, numero_facture = None, date_emission = None, montant_total = None, etat = None, numero_contrat = None):

        self.__date_emission = date_emission
        self.__montant_total = montant_total
        self.__etat = etat
        self.__numero_contrat = numero_contrat

        if numero_facture is not None : 
            self.__numero_facture = numero_facture
        else : 
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

    #Commentaire : yeahhh same things todo...

    def set_numero_facture(self, numero_facture):
        self.__numero_facture = numero_facture

    def set_date_emission(self, date_emission):
        self.__date_emission = date_emission

    def set_montant_total(self, montant_total):
        self.__montant_total = montant_total

    def set_etat(self, etat):
        self.__etat = etat
    
    def set_numero_contrat(self, numero_contrat) :
        self.__numero_contrat = numero_contrat

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