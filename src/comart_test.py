
def main():

    from domaine.Client import Client
    from domaine.Contrat import Contrat
    from domaine.Activite import Activite
    from domaine.Devis import Devis
    from domaine.Facture import Facture
    from domaine.Paiement import Paiement
    from domaine.Prestation import Prestation

    from DAO.DAOSession import DAOSession

    # Ouvrir la session DAO
    DAOSession.open()

    #insertion pour client : 
    client_1 = Client(nom="Descartes", prenom="René", adresse="Panthéon 76000" ,telephone="0123456789", courriel="D_Rere@gmail.com", enum_status_client="ANCIEN")
    
    print(client_1)

    #insertion pour contrat : 
    contrat_1 = Contrat(numero_contrat="CONT-2026-001",date_debut="2026-01-01",duree="12 mois",nb_productions_totales=12,periodicite="MENSUELLE",montant_global=5000.00,condition_paiements="Paiement en 3 fois", id_client=1)

    print(contrat_1)

    #insertion pour Devis : 

    devis_1 = Devis(numero_devis="DEV-2026-001",date_emission="2026-01-01",date_validite="2026-01-31",description_prestation="Prestation de photographie pour événement",quantite_prevue=1,details_couts="Détails des coûts estimés",montant_total_estime=1500.00,statut="EN_ATTENTE",date_acceptation=None,id_client=1,numero_contrat="CONT-2026-001")
    print(devis_1)

    #insertion pour prestation : 
    prestation_1 = Prestation(date_prevue="2026-02-15 14:00:00",date_effective=None,lieu="Paris",type_prestation="MARIAGE",nb_photos_prevues=100,nb_videos_prevues=5,numero_contrat="CONT-2026-001")

    print(prestation_1)

    #insertion pour Activité : 
    activite_1 = Activite(libelle_operationnel="Préparation du matériel",date_prevues="2026-02-14 10:00:00",date_effective=None,duree_estimee=2,responsable="Jean Dupont",statut="PREVUE",id_prestation=1)

    print(activite_1)


    DAOSession.close()

if __name__ == "__main__":

    main()
