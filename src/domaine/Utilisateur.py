from dao.DAOUtilisateur import DAOUtilisateur
from datetime import datetime

ROLES_VALIDES = {"ADMIN", "COLLABORATEUR"}
STATUTS_VALIDES = {"ACTIF", "INACTIF"}


class Utilisateur:

    leDAOUtilisateur = DAOUtilisateur.get_instance()

    def __init__(self, id_utilisateur: int = None, nom: str = None, prenom: str = None, email: str = None, mot_de_passe: str = None, role: str = None, statut: str = "ACTIF", date_creation: datetime = None, id_createur: int = None):

        # Vérification type :
        if not isinstance(nom, str):
            raise TypeError("l'attribut {nom} doit être une chaine de caractère")
        if not isinstance(prenom, str):
            raise TypeError("l'attribut {prenom} doit être une chaine de caractère")
        if not isinstance(email, str):
            raise TypeError("l'attribut {email} doit être une chaine de caractère")
        if not isinstance(mot_de_passe, str):
            raise TypeError("l'attribut {mot_de_passe} doit être une chaine de caractère")
        if id_createur is not None and not isinstance(id_createur, int):
            raise TypeError("l'attribut {id_createur} doit être un entier")

        # Vérification 
        if role not in ROLES_VALIDES:
            raise ValueError(f"l'attribut role est invalide : '{role}'. Valeurs acceptées : {ROLES_VALIDES}")
        if statut not in STATUTS_VALIDES:
            raise ValueError(f"l'attribut statut est invalide : '{statut}'. Valeurs acceptées : {STATUTS_VALIDES}")

        self.__nom = nom
        self.__prenom = prenom
        self.__email = email
        self.__mot_de_passe = mot_de_passe
        self.__role = role
        self.__statut = statut
        self.__date_creation = date_creation
        self.__id_createur = id_createur

        if id_utilisateur is not None:
            self.__id_utilisateur = id_utilisateur
        else:
            resultat = Utilisateur.leDAOUtilisateur.creer_utilisateur(
                self.__nom,
                self.__prenom,
                self.__email,
                self.__mot_de_passe,
                self.__role,
                self.__id_createur,
            )
            if resultat is not True:
                raise ValueError(f"Impossible de créer l'utilisateur")
            self.__id_utilisateur = None

    # Getters

    def get_id_utilisateur(self):
        return self.__id_utilisateur

    def get_nom(self):
        return self.__nom

    def get_prenom(self):
        return self.__prenom

    def get_email(self):
        return self.__email

    def get_role(self):
        return self.__role

    def get_statut(self):
        return self.__statut

    def get_id_createur(self):
        return self.__id_createur

    def get_date_creation(self):
        return self.__date_creation

    # Setters

    def set_nom(self, nom):
        if not isinstance(nom, str):
            raise TypeError("l'attribut {nom} doit être une chaine de caractère")
        self.__nom = nom
        Utilisateur.leDAOUtilisateur.update_utilisateur(self)

    def set_prenom(self, prenom):
        if not isinstance(prenom, str):
            raise TypeError("l'attribut {prenom} doit être une chaine de caractère")
        self.__prenom = prenom
        Utilisateur.leDAOUtilisateur.update_utilisateur(self)

    def set_email(self, email):
        if not isinstance(email, str):
            raise TypeError("l'attribut {email} doit être une chaine de caractère")
        self.__email = email
        Utilisateur.leDAOUtilisateur.update_utilisateur(self)

    def set_mot_de_passe(self, mot_de_passe):
        if not isinstance(mot_de_passe, str):
            raise TypeError("l'attribut {mot_de_passe} doit être une chaine de caractère")
        self.__mot_de_passe = mot_de_passe
        Utilisateur.leDAOUtilisateur.update_utilisateur(self)

    def set_role(self, role):
        if role not in ROLES_VALIDES:
            raise ValueError(f"l'attribut role est invalide : '{role}'. Valeurs acceptées : {ROLES_VALIDES}")
        self.__role = role
        Utilisateur.leDAOUtilisateur.update_utilisateur(self)

    def set_statut(self, statut):
        if statut not in STATUTS_VALIDES:
            raise ValueError(f"l'attribut statut est invalide : '{statut}'. Valeurs acceptées : {STATUTS_VALIDES}")
        self.__statut = statut
        Utilisateur.leDAOUtilisateur.update_utilisateur(self)

    def __str__(self):
        return f"Utilisateur(id_utilisateur={self.__id_utilisateur}, nom={self.__nom}, prenom={self.__prenom}, email={self.__email}, role={self.__role}, statut={self.__statut}, date_creation={self.__date_creation}, id_createur={self.__id_createur})"