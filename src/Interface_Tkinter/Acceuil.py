import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import time

compte_utilisateur = {
    "Client1" : {"email" : "root@gmail.com", "mdp" : "root"}
}
class ConnexionUI() :

    def __init__(self, root):

        #Création du root
        self.root = root
        self.root.title("Com'Art")
        self.root.geometry("800x400")

        #Création email, mdp, bouton connexion : 

        self.label_email = ttk.Label(self.root , text="Email : ")
        self.entry_email = ttk.Entry(self.root)

        self.label_mdp = ttk.Label(self.root, text="Mot de passe : ")
        self.entry_mdp = ttk.Entry(self.root, show="*")

        self.bouton = ttk.Button(self.root, text="Valider", command=self.verification) #commande à définir afin de vérifier le client.

        #packs : 
        self.label_email.pack(side='top', anchor='center', pady=(50, 5))
        self.entry_email.pack(side='top', anchor='center', pady=(0, 25))
        self.label_mdp.pack(side='top', anchor='center', pady=(25, 5)) 
        self.entry_mdp.pack(side='top', anchor='center', pady=(0, 50)) 
        self.bouton.pack(side='top', anchor='center', pady=(0, 75))
        
    def verification(self):
  
        email = self.entry_email.get()
        mdp = self.entry_mdp.get()
        
        if not email : 
            mb.showwarning("Champs Vide", "Veuillez renseigner votre email et mots de passe")
            return     
        
        if not mdp : 
            mb.showwarning("Champs Vide", "Veuillez renseigner votre mots de passe")
            return   

        if not ("@" and "." in email) :
            mb.showwarning("Erreur", "Email non valide")
            return
            
        valid = { client for client, identifiant  in compte_utilisateur.items() if identifiant["email"] == email and identifiant["mdp"] == mdp}

        if len(valid) <= 0 :
            self.entry_email.delete(0, tk.END)
            self.entry_mdp.delete(0, tk.END)
            mb.showwarning("identifiant FAUX ! ", "Veuillez réessayer.")
            return

        reponse = mb.showinfo("Accès Granted", " Yayyyyyyyyyy ! ")
        
        if reponse :
            self.root.destroy()


if __name__ == "__main__" :

    root = tk.Tk()

    app = ConnexionUI(root)

    root.mainloop()