#message Error value :
invalid_type = "Invalid type !"

class Client :

    def __init__(self, id_client, nom, prenom, raison_sociale, adresse, telephone, courriel, enum_type_client, enum_status_client) :
        
        self.__id_client = id_client
        self.__nom = nom
        self.__prenom = prenom
        self.__raison_sociale = raison_sociale
        self.__adresse = adresse
        self.__telephone = telephone
        self.__courriel = courriel
        self.__enum_type_client = enum_type_client
        self.__enum_status_client = enum_status_client

    # Getters :

    def get_id_client(self) :
        return self.__id_client
    
    def get_nom(self) :
        return self.__nom
    
    def get_prenom(self) : 
        return self.__prenom
    
    def get_raison_sociale(self) :
        return self.__raison_sociale
    
    def get_adresse(self) :
        return self.__adresse
    
    def get_telephone(self) :
        return self.__telephone
    
    def get_courriel(self) :
        return self.__courriel
    
    def get_enum_type_client(self) : 
        return self.__enum_type_client
    
    def get_status_client(self) :
        return self.__enum_status_client
    
    #Setters : 

    #commentaire : ptn faudra faire les verifications des setterss eazkjehazrhbahjfb

    ##commentaire : Si Zerin ne se bouge pas le cul, je vais l'enlever du projet de web.

    def set_id_client(self, id_client) : 

        if isinstance(id_client, int) :
            self.__id_client = id_client
        else : 
            raise ValueError(invalid_type)
        
    def set_nom(self, nom) : 

        if isinstance(nom, str) :
            self.__nom = nom
        else : 
            raise ValueError(invalid_type)
        
    def set_prenom(self, prenom) : 

        if isinstance(prenom, str) :
            self.__prenom = prenom
        else : 
            raise ValueError(invalid_type)
        
    def set_raison_sociale(self, raison_sociale) :

        if isinstance(raison_sociale, str) :
            self.__raison_sociale = raison_sociale
        else : 
            raise ValueError(invalid_type)
        
    def set_adresse(self, adresse) :

        if isinstance(adresse, str) :
            self.__adresse = adresse
        else : 
            raise ValueError(invalid_type)
        
    def set_telephone(self, telephone) :

        if isinstance(telephone, str) :
            self.__telephone = telephone
        else :
            raise ValueError(invalid_type)

    def set_courriel(self, courriel) :

        if isinstance(courriel, str) :
            self.__courriel = courriel
        else :
            raise ValueError(invalid_type)    
        
    def set_enum_type_client(self, enum_type_client) :

        if isinstance(enum_type_client, str) :
            self.__enum_type_client = enum_type_client
        else :
            raise ValueError(invalid_type)

    def set_enum_status_client(self, enum_status_client) :

        if isinstance(enum_status_client, str) :
            self.__enum_status_client = enum_status_client
        else :
            raise ValueError(invalid_type)       
        
    #Les Setters sont incomplet, il faudra faire des vérificaitons plus perf et approfondie.

    def __str__(self):
        return f"Client(id_client={self.__id_client}, nom={self.__nom}, prenom={self.__prenom}, raison_sociale={self.__raison_sociale}, adresse={self.__adresse}, telephone={self.__telephone}, courriel={self.__courriel}, type_client={self.__enum_type_client}, statut={self.__enum_status_client})"