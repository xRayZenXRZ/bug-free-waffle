

class DAOCompteUtilisateur : 

    unique_instance = None

    @staticmethod
    def get_instance() :
        if DAOCompteUtilisateur.unique_instance is None : 
            DAOCompteUtilisateur.unique_instance = DAOCompteUtilisateur()
        return DAOCompteUtilisateur.unique_instance
    
    def insert_compte(self , compte) :
        pass

    def delete_compte(self, compte) : 
        pass

    def find_compte(self, compte) : 
        pass

    def update_compte(self, compte):
        pass

    def find_by_login_motsDePasse(self, login, motDePasse) :
        pass

    def set_all_values(self, res):
        pass
