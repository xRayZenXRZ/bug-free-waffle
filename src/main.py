import tkinter as tk
from Interface_Tkinter.Acceuil import ConnexionUI
from Interface_Tkinter.main_windows import main_windows
from Interface_Tkinter.gestion_utilisateur import GestionUtilisateur

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Com'Art")
        self.root.geometry("800x400")

        # Container pour changer de page
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

        self.root.geometry("1000x600")
        
        main_windows(self.container, utilisateur, self.afficher_gestion_utilisateurs)

    def afficher_gestion_utilisateurs(self):
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de gestion
        GestionUtilisateur(self.container, self.utilisateur_connecte)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
