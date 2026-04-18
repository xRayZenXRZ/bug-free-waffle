class Facture : 

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
        return f"Facture(id_facture={self.__id_facture}, num_facture={self.__num_facture}, date_emission={self.__date_emission}, montant_total={self.__montant_total}, etat={self.__enum_facture_etat})"