import tkinter as tk
from Interface_Tkinter.Acceuil import ConnexionUI
from Interface_Tkinter.main_windows import main_windows
from Interface_Tkinter.gestion_utilisateur import GestionUtilisateur

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Com'Art")
        self.root.geometry("800x400")

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
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page de gestion des utilisateurs
        GestionUtilisateur(self.container, self.utilisateur_connecte, self.afficher_main_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
