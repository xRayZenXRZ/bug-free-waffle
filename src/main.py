from Interface_Tkinter.gestion_client import GestionClient
from Interface_Tkinter.main_windows import MainWindow
from Interface_Tkinter.Acceuil import ConnexionUI
import tkinter as tk
from Interface_Tkinter.gestion_utilisateur import GestionUtilisateur
from Interface_Tkinter.gestion_devis import GestionDevis


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Com'Art")
        self.root.geometry("800x400")

        # Container
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Utilisateur connecté
        self.utilisateur_connecte = None

        # Démarrer avec connexion
        ConnexionUI(self.container, self.afficher_main_window)

    def afficher_main_window(self, utilisateur):
        self.utilisateur_connecte = utilisateur

        # Nettoyer
        for widget in self.container.winfo_children():
            widget.destroy()

        # Agrandir la fenêtre
        self.root.geometry("1000x600")

        # Afficher main window
        MainWindow(self.container, utilisateur,
<<<<<<< HEAD
                   self.afficher_gestion_utilisateurs,self.afficher_gestion_clients)
=======
                   self.afficher_gestion_utilisateurs,self.afficher_gestion_clients,self.afficher_gestion_devis)
>>>>>>> Clement

    def afficher_gestion_utilisateurs(self):
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de gestion
<<<<<<< HEAD
        GestionUtilisateur(self.container, self.utilisateur_connecte)
=======
        GestionUtilisateur(self.container, self.utilisateur_connecte,on_back=lambda: self.afficher_main_window(self.utilisateur_connecte))
>>>>>>> Clement
        
    def afficher_gestion_clients(self):
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de gestion
<<<<<<< HEAD
        GestionClient(self.container, self.utilisateur_connecte)
=======
        GestionClient(self.container, self.utilisateur_connecte,on_back=lambda: self.afficher_main_window(self.utilisateur_connecte))
        
    def afficher_gestion_devis(self):
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de gestion
        GestionDevis(self.container, self.utilisateur_connecte,on_back=lambda: self.afficher_main_window(self.utilisateur_connecte))
>>>>>>> Clement


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
