from dao.DAOActivite import DAOActivite
from domaine.Activite import Activite
from dao.DAOCollaborateur import DAOCollaborateur

class Collaborateur:

    leDAOCollaborateur = DAOCollaborateur.get_instance()
    leDAOActivite = DAOActivite.get_instance()

    def __init__(self, id_collaborateur: int = None , nom: str = None, prenom: str = None,poste: str = None, telephone_pro: str = None, numero_devis: str = None, id_utilisateur: int = None):

        self.__nom = nom
        self.__prenom = prenom
        self.__poste = poste
        self.__telephone_pro = telephone_pro
        self.__numero_devis = numero_devis
        self.__id_utilisateur = id_utilisateur

        self.__les_activites = []

        if id_collaborateur is not None :
            self.__id_collaborateur = id_collaborateur
        else:
            self.__id_collaborateur = Collaborateur.leDAOCollaborateur.insert_collaborateur(self)

    # Méthodes statiques

    @staticmethod
    def charger(id_collaborateur):
        un_collaborateur = Collaborateur.leDAOCollaborateur.find_collaborateur(id_collaborateur)
        un_activite = Activite(-1)
        un_activite.set_id_collaborateur(id_collaborateur=id_collaborateur)
        un_collaborateur.set_les_activites(Collaborateur.leDAOActivite.select_activite(un_activite))
        return un_collaborateur

    @staticmethod
    def supprimer(un_collaborateur):
        if un_collaborateur.get_les_activites() :
            raise Exception("Erreur_suppression_collaborateur_avec_activite")
        else :
            Collaborateur.leDAOCollaborateur.delete_collaborateur(un_collaborateur)
    
    # Getters

    def get_id_collaborateur(self):
        return self.__id_collaborateur

    def get_nom(self):
        return self.__nom

    def get_prenom(self):
        return self.__prenom

    def get_poste(self):
        return self.__poste

    def get_telephone_pro(self):
        return self.__telephone_pro

    def get_numero_devis(self):
        return self.__numero_devis

    def get_id_utilisateur(self):
        return self.__id_utilisateur

    def get_les_activites(self):
        return self.__les_activites

    # Setters

    def set_nom(self, nom: str):
        if not isinstance(nom, str) or not nom.strip():
            raise ValueError("Le nom doit être une chaîne non vide.")
        self.__nom = nom
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_prenom(self, prenom: str):
        if not isinstance(prenom, str) or not prenom.strip():
            raise ValueError("Le prénom doit être une chaîne non vide.")
        self.__prenom = prenom
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_poste(self, poste: str):
        if not isinstance(poste, str):
            raise TypeError("L'attribut poste doit être une chaîne de caractères.")
        self.__poste = poste
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_telephone_pro(self, telephone_pro: str):
        if not isinstance(telephone_pro, str):
            raise TypeError("L'attribut telephone_pro doit être une chaîne de caractères.")
        self.__telephone_pro = telephone_pro
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_numero_devis(self, numero_devis: str):
        self.__numero_devis = numero_devis
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_id_utilisateur(self, id_utilisateur: int):
        """Associe un compte Utilisateur existant à ce collaborateur."""
        self.__id_utilisateur = id_utilisateur
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_les_activites(self, les_activites: list):
        self.__les_activites = les_activites


    def __str__(self):
        return (f"Collaborateur(id={self.__id_collaborateur}, nom={self.__nom}, prenom={self.__prenom}, poste={self.__poste}, tel={self.__telephone_pro}, numero_devis={self.__numero_devis} ,id_utilisateur={self.__id_utilisateur})")