from domaine.Client import Client

import csv

from domaine.Prestation import Prestation

def importation_clients_csv():

    clients = Client.leDAOClient.select_client()

    fichier_texte = "src/Interface_Tkinter/importation/client/clients.txt"
    fichier_csv = "src/Interface_Tkinter/importation/client/clients.csv"
    
    with open(fichier_texte, "w", encoding="utf;8") as client_file : 
        client_file.write("idClient;type_client;nom;prenom;raisonSociale;adressePostale;telephone;email;statut")
        for x in clients : 
            if(x.get_raison_sociale() is not None) :
                ligne = (f"{x.get_id_client()};ENTREPRISE;{x.get_nom()};{x.get_prenom()};{x.get_raison_sociale()};{x.get_adresse()};{x.get_telephone()};{x.get_courriel()};{x.get_status_client()}").strip()
                client_file.write("\n"+ligne)
            else : 
                ligne = (f"{x.get_id_client()};PARTICULIER;{x.get_nom()};{x.get_prenom()};{x.get_raison_sociale()};{x.get_adresse()};{x.get_telephone()};{x.get_courriel()};{x.get_status_client()}").strip()
                client_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf;8") as client_file : 
        lignes = client_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf;8") as client_file_csv:
        writer = csv.writer(client_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def importation_prestations_csv():
    
    prestations = Prestation.leDAOPrestation.select_prestation()

    fichier_texte = "src/Interface_Tkinter/importation/prestation/prestations.txt"
    fichier_csv = "src/Interface_Tkinter/importation/prestation/prestations.csv"

    with open(fichier_texte, "w", encoding="utf;8") as prestation_file : 
        prestation_file.write("idPrestation;datePrevue;dateEffective;lieu;type;nbPhotosPrevues;nbVideosPrevues;numeroContrat")
        for x in prestations : 
            ligne = (f"{x.get_id_prestation()};{x.get_date_prevue()};{x.get_date_effective()};{x.get_lieu()};{x.get_type()};{x.get_nb_photos_prevues()};{x.get_nb_videos_prevues()};{x.get_numero_contrat()}").strip()
            prestation_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf;8") as prestation_file : 
        lignes = prestation_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf;8") as prestation_file_csv:
        writer = csv.writer(prestation_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")








if __name__ == "__main__" :
    importation_prestations_csv()
