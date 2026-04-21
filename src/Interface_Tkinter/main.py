import tkinter as tk
from Acceuil import ConnexionUI
from main_windows import main_windows


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Com'Art")
        self.root.geometry("800x400")

        # Container pour changer de page
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Démarrer avec la page de connexion
        ConnexionUI(self.container, self.afficher_acceuil_connecte)

    def afficher_acceuil_connecte(self, nom_utilisateur, email):
        # Nettoyer la page actuelle
        for widget in self.container.winfo_children():
            widget.destroy()

        # Afficher la page d'accueil connecté
        main_windows(self.container, nom_utilisateur)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
