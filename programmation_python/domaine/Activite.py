from dao.DAOActivite import DAOActivite
from datetime import datetime

class Activite:

    leDAOActivite = DAOActivite()

    def __init__(self, id_activite: int = None, libelle_operationnel: str = None, date_prevues: str = None, date_effective: str = None, duree_estimee: int = None, id_collaborateur: int = None, statut: str = None, id_prestation: int = None):

        self.__libelle_operationnel = libelle_operationnel
        self.__date_prevues = date_prevues
        self.__date_effective = date_effective
        self.__duree_estimee = duree_estimee
        self.__id_collaborateur = id_collaborateur
        self.__statut = statut
        self.__id_prestation = id_prestation

        if id_activite is not None:
            self.__id_activite = id_activite
        else:
            self.__id_activite = Activite.leDAOActivite.insert_activite(self)

    @staticmethod
    def charger(id_activite):
        return Activite.leDAOActivite.find_activite(id_activite)

    @staticmethod
    def supprimer(un_activite):
        if un_activite.get_id_activite() is None : 
            Activite.leDAOActivite.delete_activite(un_activite)
        else : 
            raise Exception("Erreur_suppression_activite_avec_prestation")
    

    # Getters :

    def get_id_activite(self):
        return self.__id_activite

    def get_libelle_operationnel(self):
        return self.__libelle_operationnel

    def get_date_prevues(self):
        return self.__date_prevues

    def get_date_effective(self):
        return self.__date_effective

    def get_duree_estimee(self):
        return self.__duree_estimee

    def get_id_collaborateur(self):
        return self.__id_collaborateur

    def get_statut(self):
        return self.__statut

    def get_id_prestation(self):
        return self.__id_prestation

    # Setters

    def set_id_activite(self, id_activite):
        if not isinstance(id_activite, int):
            raise TypeError(f"l'attribut {id_activite} doit être un entier")
        
        self.__id_activite = id_activite
        Activite.leDAOActivite.update_activite(self)

    def set_libelle_operationnel(self, libelle_operationnel):
        if not isinstance(libelle_operationnel, str):
            raise TypeError(f"l'attribut {libelle_operationnel} doit être une chaine de caractère")
        
        self.__libelle_operationnel = libelle_operationnel
        Activite.leDAOActivite.update_activite(self)

    def set_date_prevues(self, date_prevues):
        if not isinstance(date_prevues, str) and self.is_date(date_prevues):
            raise TypeError(f"l'attribut {date_prevues} doit être une chaine de caractère")
        
        self.__date_prevues = date_prevues
        Activite.leDAOActivite.update_activite(self)

    def set_date_effective(self, date_effective):
        if not isinstance(date_effective, str) and self.is_date(date_effective):
            raise TypeError(f"l'attribut {date_effective} doit être une chaine de caractère")

        self.__date_effective = date_effective
        Activite.leDAOActivite.update_activite(self)

    def set_duree_estimee(self, duree_estimee):
        if not isinstance(duree_estimee, int):
            raise TypeError(f"l'attribut {duree_estimee} doit être un entier")
        
        self.__duree_estimee = duree_estimee
        Activite.leDAOActivite.update_activite(self)

    def set_id_collaborateur(self, id_collaborateur):
        if not isinstance(id_collaborateur, int):
            raise TypeError(f"l'attribut {id_collaborateur} doit être un entier")
        
        self.__id_collaborateur = id_collaborateur
        Activite.leDAOActivite.update_activite(self)

    def set_statut(self, statut):
        if not isinstance(statut, str):  # à verifier if in enum
            raise TypeError(f"l'attribut {statut} doit être une chaine de caractère")
        
        self.__statut = statut
        Activite.leDAOActivite.update_activite(self)

    def set_id_prestation(self, id_prestation):
        if not isinstance(id_prestation, int):
            raise TypeError(f"l'attribut {id_prestation} doit être un entier")
        
        self.__id_prestation = id_prestation
        Activite.leDAOActivite.update_activite(self)

    def is_date(self, str_date : str) -> bool :
        format = "%Y-%m-%d"
        res = bool(datetime.strptime(str_date, format))
        if res is False : 
            raise ValueError(f"l'attributs doit être sous le format 'yyyy-mm-dd'")
        return res

    def __str__(self):
        return f"Activite(id_activite={self.__id_activite}, libelle_operationnel={self.__libelle_operationnel}, date_prevues={self.__date_prevues}, date_effective={self.__date_effective}, duree_estimee={self.__duree_estimee}, id_collaborateur={self.__id_collaborateur}, statut={self.__statut}, id_prestation={self.__id_prestation})"
    