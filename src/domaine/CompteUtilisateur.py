class Compte_Utilisateur :

    def __init__(self, id_compte_utilisateur, login, mot_de_passe, type_utilisateur, id_client):
        self.__id_compte_utilisateur = id_compte_utilisateur
        self.__login = login
        self.__mot_de_passe = mot_de_passe
        self.__type_utilisateur = type_utilisateur
        self.__id_client = id_client #particulier | entreprise

    # Getters
    def get_id_compte_utilisateur(self):
        return self.__id_compte_utilisateur

    def get_login(self):
        return self.__login

    def get_mot_de_passe(self):
        return self.__mot_de_passe

    def get_type_utilisateur(self):
        return self.__type_utilisateur

    def get_id_client(self):
        return self.__id_client

    # Setters

    #commentaire : todo 
    def set_id_compte_utilisateur(self, id_compte_utilisateur):
        self.__id_compte_utilisateur = id_compte_utilisateur

    def set_login(self, login):
        self.__login = login

    def set_mot_de_passe(self, mot_de_passe):
        self.__mot_de_passe = mot_de_passe

    def set_type_utilisateur(self, type_utilisateur):
        self.__type_utilisateur = type_utilisateur

    def set_id_client(self, id_client):
        self.__id_client = id_client

    def __str__(self):
        return f"Compte_Utilisateur(id_compte_utilisateur={self.__id_compte_utilisateur}, login={self.__login}, type_utilisateur={self.__type_utilisateur}, id_client={self.__id_client})"