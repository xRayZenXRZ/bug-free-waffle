<<<<<<< HEAD
from Interface_Tkinter.gestion_client import GestionClient
from Interface_Tkinter.main_windows import MainWindow
from Interface_Tkinter.Acceuil import ConnexionUI
import tkinter as tk
from Interface_Tkinter.gestion_utilisateur import GestionUtilisateur
from Interface_Tkinter.gestion_devis import GestionDevis

=======
import tkinter as tk
from Interface_Tkinter.Acceuil import ConnexionUI
from Interface_Tkinter.main_windows import main_windows
from Interface_Tkinter.gestion_utilisateur import GestionUtilisateur
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Com'Art")
        self.root.geometry("800x400")

<<<<<<< HEAD
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
                   self.afficher_gestion_utilisateurs,self.afficher_gestion_clients,self.afficher_gestion_devis)

    def afficher_gestion_utilisateurs(self):
=======
        # Container principal pour changer de page
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Utilisateur actuellement connecté
        self.utilisateur_connecte = None

        # Démarrer avec la page de connexion
        self.afficher_connexion()

    def afficher_connexion(self):
        """Affiche la page de connexion."""
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de connexion
        ConnexionUI(self.container, self.afficher_main_window)

    def afficher_main_window(self, utilisateur):
        """Affiche la page principale après la connexion."""
        self.utilisateur_connecte = utilisateur

        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Redimensionner la fenêtre
        self.root.geometry("1000x600")

        # Afficher la page principale
        main_windows(self.container, utilisateur, self.afficher_gestion_utilisateurs)

    def afficher_gestion_utilisateurs(self):
        """Affiche la page de gestion des utilisateurs."""
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

<<<<<<< HEAD
        # Afficher la page de gestion
        GestionUtilisateur(self.container, self.utilisateur_connecte,on_back=lambda: self.afficher_main_window(self.utilisateur_connecte))
        
    def afficher_gestion_clients(self):
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de gestion
        GestionClient(self.container, self.utilisateur_connecte,on_back=lambda: self.afficher_main_window(self.utilisateur_connecte))
        
    def afficher_gestion_devis(self):
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de gestion
        GestionDevis(self.container, self.utilisateur_connecte,on_back=lambda: self.afficher_main_window(self.utilisateur_connecte))
=======
        # Afficher la page de gestion des utilisateurs
        GestionUtilisateur(self.container, self.utilisateur_connecte, self.afficher_main_window)
>>>>>>> 6fe10fa5ff6b8e26b6e3f701207ed2a97653e357


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
