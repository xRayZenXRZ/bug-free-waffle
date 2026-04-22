from dao.DAOUtilisateur import DAOUtilisateur
from dao.DAOClient import DAOClient

class Utilisateur:
    
    leDAOUtilisateur = DAOUtilisateur.get_instance()
    leDAOClient = DAOClient.get_instance()   
    
    def __init__(self, idCompteUtilisateur=None, email = None, motDePasse = None, typeUtilisateur = None, client = None):
        self.idCompteUtilisateur = idCompteUtilisateur
        self.email = email
        self.motDePasse = motDePasse
        self.typeUtilisateur = typeUtilisateur
        if typeUtilisateur == "CLIENT":
            self.client = client
        else:
            self.client = None
        if idCompteUtilisateur is not None:
            self.idCompteUtilisateur = idCompteUtilisateur
        else:
            self.idCompteUtilisateur = Utilisateur.leDAOUtilisateur.insert_compte(self)
    
    """def charger(idCompte):
        return CompteUtilisateur.leDAOUtilisateur.find_compte(idCompte)
    
    def chargerAvecEmailMdp(email, motDePasse):
        return CompteUtilisateur.leDAOUtilisateur.find_by_login_motDePasse(email, motDePasse)"""
    
    def supprimer(unCompte):
        Utilisateur.leDAOUtilisateur.delete_compte(unCompte)
    
    def get_idCompteUtilisateur(self):
        return self.idCompteUtilisateur
    
    def set_idCompteUtilisateur(self, idCompteUtilisateur):
        self.idCompteUtilisateur = idCompteUtilisateur
        Utilisateur.leDAOUtilisateur.update_compte(self)
    
    def get_email(self):
        return self.email
    
    def set_email(self, email):
        self.email = email
        Utilisateur.leDAOUtilisateur.update_compte(self)
    
    def get_motDePasse(self):
        return self.motDePasse
   
    def set_motDePasse(self, motDePasse):
        self.motDePasse = motDePasse
        Utilisateur.leDAOUtilisateur.update_compte(self)
    
    def get_typeUtilisateur(self):
        return self.typeUtilisateur
   
    def set_typeUtilisateur(self, typeUtilisateur):
        self.typeUtilisateur = typeUtilisateur
        Utilisateur.leDAOUtilisateur.update_compte(self)
    
    def get_client(self):
        return self.client
    
    def set_client(self, client):
        if self.typeUtilisateur != "CLIENT":
            raise Exception("Erreur_Utilisateur_Non_Client")
        self.client = client
        Utilisateur.leDAOUtilisateur.update_compte(self)

    def __str__(self):
        return f"Utilisateur [idUtilisateur={self.idCompteUtilisateur}, email={self.email}, motDePasse={self.motDePasse}, typeUtilisateur={self.typeUtilisateur}, client={self.client}]"