from DAO.DAOPaiement import DAOPAiement

class Paiement :

    leDAOPaiement = DAOPAiement.get_instance()

    def __int__(self, id_paiement = None, date = None, montant = None, numero_Facture = None):

        self.__date = date
        self.__montant = montant
        self.__numero_Facture = numero_Facture

        if id_paiement is not None : 
            self.__id_paiement = id_paiement
        else : 
            self.__id_paiement = Paiement.leDAOPaiement.insert_paiement(self)


    # Getters
    def get_id_paiement(self):
        return self.__id_paiement

    def get_montant(self):
        return self.__montant
    
    def get_date(self):
        return self.__date
    
    def get_numero_Facture(self) :
        return self.__numero_Facture


    # Setters 
    
    def set_id_paiement(self, id_paiement):
        self.__id_paiement = id_paiement

    def set_date(self, date) : 
        self.__date = date

    def set_montant(self, montant):
        self.__montant = montant
    
    def set_numeroFacture(self, numero_Facture) :
        self.__numero_Facture = numero_Facture

    def __str__(self):
        return f"Paiement(id_paiement={self.__id_paiement},date={self.__date}, montant={self.__montant}, numeroFacture={self.__numeroFacture})"


"""class Paiement :

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

    def __str__(self):
        return f"Paiement(id_paiement={self.__id_paiement}, montant={self.__montant}, conditions_paiements={self.__enum_paiements_conditions})"""