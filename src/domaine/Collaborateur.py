from domaine.Utilisateur import Utilisateur
from dao.DAOCollaborateur import DAOCollaborateur

class Collaborateur(Utilisateur):

    leDAOCollaborateur = DAOCollaborateur.get_instance()

    def __init__(self, id_collaborateur: int = None, poste: str = None, telephone_pro: str = None, **kwargs):
        
        if 'role' not in kwargs:
            kwargs['role'] = "COLLABORATEUR"

        super().__init__(**kwargs) #kwargs sert à récupere tous les attributs du classe hérité

        self.__poste = poste
        self.__telephone_pro = telephone_pro

        self.__les_activites = []

        if id_collaborateur is not None:
            self.__id_collaborateur = id_collaborateur
        else:
            id_user = self.get_id_utilisateur()
            
            if id_user is None:
                raise ValueError("Erreur critique : L'ID utilisateur est introuvable. Vérifiez que DAOUtilisateur renvoie bien l'ID après création.")

            # Création en base
            succes, resultat = Collaborateur.leDAOCollaborateur.creer_collaborateur(id_user, self.__poste, self.__telephone_pro)
            
            if succes is not True:
                raise ValueError(f"Impossible de créer le collaborateur : {resultat}")
            
            self.__id_collaborateur = resultat

    #methode statiques : 

    @staticmethod
    def charger( id_collaborateur ):
        pass

    @staticmethod
    def supprimer( un_collaborateur ) :
        pass


    # Getters

    def get_id_collaborateur(self):
        return self.__id_collaborateur

    def get_poste(self):
        return self.__poste

    def get_telephone_pro(self):
        return self.__telephone_pro
    
    def get_les_activites(self) :
        return self.__les_activites

    # Setters

    def set_poste(self, poste):
        if not isinstance(poste, str):
            raise TypeError("L'attribut poste doit être une chaîne de caractères")
        self.__poste = poste
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_telephone_pro(self, telephone_pro):
        if not isinstance(telephone_pro, str):
            raise TypeError("L'attribut telephone_pro doit être une chaîne de caractères")
        self.__telephone_pro = telephone_pro
        Collaborateur.leDAOCollaborateur.update_collaborateur(self)

    def set_les_activites(self, les_activites) :
        self.__les_activites = les_activites

    # Méthode d'affichage

    def __str__(self):
        parent_str = super().__str__()
        return f"Collaborateur({parent_str}, id_collaborateur={self.__id_collaborateur}, poste={self.__poste}, telephone_pro={self.__telephone_pro})"