import tkinter as tk
from Acceuil import ConnexionUI
from main_windows import MainWindow  # Import modifié ici


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
        MainWindow(self.container, utilisateur)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
