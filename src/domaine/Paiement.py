class Paiement :

    def __int__(self, id_paiement, montant, enum_paiements_conditions ):
        self.__id_paiement = id_paiement
        self.__montant = montant
        self.__enum_paiements_conditions = enum_paiements_conditions

    # Getters
    def get_id_paiement(self):
        return self.__id_paiement

    def get_montant(self):
        return self.__montant

    def get_enum_paiements_conditions(self):
        return self.__enum_paiements_conditions

    # Setters

    #commentaire : toujours la même chose à faire ...
    
    def set_id_paiement(self, id_paiement):
        self.__id_paiement = id_paiement

    def set_montant(self, montant):
        self.__montant = montant

    def set_enum_paiements_conditions(self, enum_paiements_conditions):
        self.__enum_paiements_conditions = enum_paiements_conditions