from domaine.Activite import Activite
from domaine.Collaborateur import Collaborateur
from domaine.Paiement import Paiement
from domaine.Client import Client

import csv

from domaine.Contrat import Contrat
from domaine.Devis import Devis
from domaine.Facture import Facture
from domaine.Prestation import Prestation

def importation_clients_csv():

    clients = Client.leDAOClient.select_client()

    fichier_texte = "src/Interface_Tkinter/importation/client/clients.txt"
    fichier_csv = "src/Interface_Tkinter/importation/client/clients.csv"
    
    with open(fichier_texte, "w", encoding="utf=8") as client_file : 
        client_file.write("idClient;type_client;nom;prenom;raisonSociale;adressePostale;telephone;email;statut")
        for x in clients : 
            if(x.get_raison_sociale() is not None) :
                ligne = (f"{x.get_id_client()};ENTREPRISE;{x.get_nom()};{x.get_prenom()};{x.get_raison_sociale()};{x.get_adresse()};{x.get_telephone()};{x.get_courriel()};{x.get_status_client()}").strip()
                client_file.write("\n"+ligne)
            else : 
                ligne = (f"{x.get_id_client()};PARTICULIER;{x.get_nom()};{x.get_prenom()};{x.get_raison_sociale()};{x.get_adresse()};{x.get_telephone()};{x.get_courriel()};{x.get_status_client()}").strip()
                client_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as client_file : 
        lignes = client_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as client_file_csv:
        writer = csv.writer(client_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def importation_prestations_csv():
    
    prestations = Prestation.leDAOPrestation.select_prestation()

    fichier_texte = "src/Interface_Tkinter/importation/prestation/prestations.txt"
    fichier_csv = "src/Interface_Tkinter/importation/prestation/prestations.csv"

    with open(fichier_texte, "w", encoding="utf=8") as prestation_file : 
        prestation_file.write("idPrestation;datePrevue;dateEffective;lieu;type;nbPhotosPrevues;nbVideosPrevues;numeroContrat")
        for x in prestations : 
            ligne = (f"{x.get_id_prestation()};{x.get_date_prevue()};{x.get_date_effective()};{x.get_lieu()};{x.get_type()};{x.get_nb_photos_prevues()};{x.get_nb_videos_prevues()};{x.get_numero_contrat()}").strip()
            prestation_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as prestation_file : 
        lignes = prestation_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as prestation_file_csv:
        writer = csv.writer(prestation_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def importations_factures_csv():

    factures = Facture.leDAOFacture.select_facture()

    fichier_texte = "src/Interface_Tkinter/importation/facture/factures.txt"
    fichier_csv = "src/Interface_Tkinter/importation/facture/factures.csv"

    with open(fichier_texte, "w", encoding="utf=8") as facture_file : 
        facture_file.write("numeroFacture;dateEmission;montantTotal;etat;numeroContrat")
        for x in factures : 
            ligne = (f"{x.get_numero_facture()};{x.get_date_emission()};{x.get_montant_total()};{x.get_etat()};{x.get_numero_contrat()}").strip()
            facture_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as facture_file : 
        lignes = facture_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as facture_file_csv:
        writer = csv.writer(facture_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def importation_contrat_csv():

    contrats = Contrat.leDAOContrat.select_contrat()

    fichier_texte = "src/Interface_Tkinter/importation/contrat/contrats.txt"
    fichier_csv = "src/Interface_Tkinter/importation/contrat/contrats.csv"

    with open(fichier_texte, "w", encoding="utf=8") as contrat_file : 
        contrat_file.write("numeroContrat;dateDebut;duree;nbProductionsTotales;periodicite;montantGlobal;conditionsPaiement;idClient")
        for x in contrats :
            ligne = (f"{x.get_numero_contrat()};{x.get_date_debut()};{x.get_duree()};{x.get_nb_productions_totales()};{x.get_periodicite()};{x.get_montant_global()};{x.get_condition_paiements()};{x.get_id_client()}").strip()
            contrat_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as contrat_file : 
        lignes = contrat_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as contrat_file_csv:
        writer = csv.writer(contrat_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def importation_devis_csv():

    devis = Devis.leDAODevis.select_devis()

    fichier_texte = "src/Interface_Tkinter/importation/devis/devis.txt"
    fichier_csv = "src/Interface_Tkinter/importation/devis/devis.csv"

    with open(fichier_texte, "w", encoding="utf=8") as devis_file : 
        devis_file.write("numeroDevis;dateEmission;dateValidite;descriptionPrestation;quantitePrevue;detailsCouts;montantTotalEstime;statut;dateAcceptation;idClient;numeroContrat")
        for x in devis :
            ligne = (f"{x.get_numero_devis()};{x.get_date_emission()};{x.get_date_validite()};{x.get_description_prestation()};{x.get_quantite_prevue()};{x.get_details_couts()};{x.get_montant_total_estime()};{x.get_statut()};{x.get_date_acceptation()};{x.get_id_client()};{x.get_numero_contrat()}").strip()
            devis_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as devis_file : 
        lignes = devis_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as devis_file_csv:
        writer = csv.writer(devis_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def importation_paiement_csv():

    paiements = Paiement.leDAOPaiement.select_paiement()

    fichier_texte = "src/Interface_Tkinter/importation/paiement/paiements.txt"
    fichier_csv = "src/Interface_Tkinter/importation/paiement/paiements.csv"

    with open(fichier_texte, "w", encoding="utf=8") as paiement_file : 
        paiement_file.write("idPaiement;datePaiement;montantPaye;numeroFacture")
        for x in paiements :
            ligne = (f"{x.get_id_paiement()};{x.get_date()};{x.get_montant()};{x.get_numero_facture()}").strip()
            paiement_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as paiement_file : 
        lignes = paiement_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as paiement_file_csv:
        writer = csv.writer(paiement_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def importation_activite_csv():

    activites = Activite.leDAOActivite.select_activite()

    fichier_texte = "src/Interface_Tkinter/importation/activite/activites.txt"
    fichier_csv = "src/Interface_Tkinter/importation/activite/activites.csv"

    with open(fichier_texte, "w", encoding="utf=8") as activite_file : 
        activite_file.write("idActivite;libelleOperationnel;datePrevue;dateEffective;dureeEstimeeHeures;statut;idCollaborateur;idPrestation")
        for x in activites :
            ligne = (f"{x.get_id_activite()};{x.get_libelle_operationnel()};{x.get_date_prevues()};{x.get_date_effective()};{x.get_duree_estimee()};{x.get_statut()};{x.get_id_collaborateur()};{x.get_statut()};{x.get_id_prestation()}").strip()
            activite_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as activite_file : 
        lignes = activite_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as activite_file_csv:
        writer = csv.writer(activite_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")

def imporatation_collaborateur_csv():

    collaborateurs = Collaborateur.leDAOCollaborateur.select_collaborateur()

    fichier_texte = "src/Interface_Tkinter/importation/collaborateur/collaborateurs.txt"
    fichier_csv = "src/Interface_Tkinter/importation/collaborateur/collaborateurs.csv"

    with open(fichier_texte, "w", encoding="utf=8") as collaborateur_file : 
        collaborateur_file.write("idCollaborateur;nom;prenom;poste;telephonePro;numeroDevis;idUtilisateur")
        for x in collaborateurs :
            ligne = (f"{x.get_id_collaborateur()};{x.get_nom()};{x.get_prenom()};{x.get_poste()};{x.get_telephone_pro()};{x.get_numero_devis()};{x.get_id_utilisateur()}").strip()
            collaborateur_file.write("\n"+ligne)
    
    print(f"Le fichier {fichier_texte} a été créé avec succès.")
    
    with open(fichier_texte, "r", encoding="utf=8") as collaborateur_file : 
        lignes = collaborateur_file.readlines()
                
    donnees = [ligne.strip().split(";") for ligne in lignes]

    with open(fichier_csv, "w", newline="", encoding="utf=8") as collaborateur_file_csv:
        writer = csv.writer(collaborateur_file_csv)
        writer.writerows(donnees)

    print(f"Le fichier {fichier_csv} a été créé avec succès.")


def importation_all_csv():
    imporatation_collaborateur_csv()
    importation_clients_csv()
    importation_activite_csv()
    importation_contrat_csv()
    importation_devis_csv()
    importation_paiement_csv()
    importations_factures_csv()
    importation_prestations_csv()

if __name__ == "__main__" :
    importation_all_csv()