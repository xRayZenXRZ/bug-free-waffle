--  Com'Art – Requêtes SELECT utilisées dans les DAOs

USE test_comart;



--  DAOClient  (src/dao/DAOClient.py)


-- find_client : 
SELECT * FROM Client WHERE idClient = 1;

-- select_client (sans critère) : liste complète
SELECT * FROM Client;

-- select_client (avec critères dynamiques) – exemples représentatifs
SELECT * FROM Client WHERE idClient = 1;

SELECT * FROM Client WHERE nom = 'Martin';

SELECT * FROM Client WHERE prenom = 'Sophie';

SELECT * FROM Client WHERE raisonSociale = 'PhotoPro SAS';

SELECT * FROM Client WHERE adressePostale = '12 Rue de Rivoli, 75004 Paris';

SELECT * FROM Client WHERE telephone = '0612345678';

SELECT * FROM Client WHERE email = 'sophie.martin@email.com';

SELECT * FROM Client WHERE statut = 'CLIENT';

-- combinaison de critères (AND dynamique)
SELECT * FROM Client WHERE nom = 'Martin' AND statut = 'CLIENT';



--  DAOCollaborateur  (src/dao/DAOCollaborateur.py)


-- find_collaborateur : 
SELECT * FROM Collaborateur WHERE idCollaborateur = 1;

-- select_collaborateur (sans critère)
SELECT * FROM Collaborateur;

-- select_collaborateur 
SELECT * FROM Collaborateur WHERE idCollaborateur = 1;

SELECT * FROM Collaborateur WHERE nom = 'Martin';

SELECT * FROM Collaborateur WHERE prenom = 'Sophie';

SELECT * FROM Collaborateur WHERE poste = 'Photographe Senior';

SELECT * FROM Collaborateur WHERE telephonePro = '0601010101';

SELECT * FROM Collaborateur WHERE numeroDevis = 'DEV-2026-001';

SELECT * FROM Collaborateur WHERE idUtilisateur = 3;

-- combinaison
SELECT * FROM Collaborateur WHERE nom = 'Dubois' AND poste = 'Responsable Vidéo';



--  DAOContrat  (src/dao/DAOContrat.py)


-- find_contrat : 
SELECT * FROM Contrat WHERE numeroContrat = 'CONT-2026-001';

-- select_contrat (sans critère)
SELECT * FROM Contrat;

-- select_contrat 
SELECT * FROM Contrat WHERE numeroContrat = 'CONT-2026-001';

SELECT * FROM Contrat WHERE dateDebut = '2026-01-01';

SELECT * FROM Contrat WHERE duree = '12 mois';

SELECT * FROM Contrat WHERE nbProductionsTotales = 12;

SELECT * FROM Contrat WHERE periodicite = 'MENSUELLE';

SELECT * FROM Contrat WHERE montantGlobal = 1500.00;

SELECT * FROM Contrat WHERE idClient = 1;

-- combinaison
SELECT * FROM Contrat WHERE periodicite = 'MENSUELLE' AND idClient = 2;



--  DAODevis  (src/dao/DAODevis.py)


-- find_devis : 
SELECT * FROM Devis WHERE numeroDevis = 'DEV-2026-001';

-- select_devis (sans critère)
SELECT * FROM Devis;

-- select_devis 
SELECT * FROM Devis WHERE numeroDevis = 'DEV-2026-001';

SELECT * FROM Devis WHERE dateEmission = '2026-01-01';

SELECT * FROM Devis WHERE dateValidite = '2026-01-31';

SELECT * FROM Devis WHERE quantitePrevue = 1;

SELECT * FROM Devis WHERE montantTotalEstime = 1500.00;

SELECT * FROM Devis WHERE statut = 'EN_ATTENTE';

SELECT * FROM Devis WHERE dateAcceptation = '2026-02-12';

SELECT * FROM Devis WHERE idClient = 1;

SELECT * FROM Devis WHERE numeroContrat = 'CONT-2026-001';

-- combinaison
SELECT * FROM Devis WHERE statut = 'ACCEPTE' AND idClient = 2;



--  DAOPrestation  (src/dao/DAOPrestation.py)


-- find_prestation : 
SELECT * FROM Prestation WHERE idPrestation = 1;

-- select_prestation (sans critère)
SELECT * FROM Prestation;

-- select_prestation 
SELECT * FROM Prestation WHERE idPrestation = 1;

SELECT * FROM Prestation WHERE datePrevue = '2026-02-15 14:00:00';

SELECT * FROM Prestation WHERE dateEffective = '2026-03-01 10:00:00';

SELECT * FROM Prestation WHERE lieu = 'Paris';

SELECT * FROM Prestation WHERE type = 'MARIAGE';

SELECT * FROM Prestation WHERE nbPhotosPrevues = 100;

SELECT * FROM Prestation WHERE nbVideosPrevues = 5;

SELECT * FROM Prestation WHERE numeroContrat = 'CONT-2026-001';

-- combinaison
SELECT * FROM Prestation WHERE type = 'MARIAGE' AND numeroContrat = 'CONT-2026-003';



--  DAOActivite  (src/dao/DAOActivite.py)


-- find_activite : 
SELECT * FROM Activite WHERE idActivite = 1;

-- select_activite (sans critère)
SELECT * FROM Activite;

-- select_activite 
SELECT * FROM Activite WHERE idActivite = 1;

SELECT * FROM Activite WHERE libelleOperationnel = 'Retouches photos';

SELECT * FROM Activite WHERE datePrevue = '2026-03-02 14:00:00';

SELECT * FROM Activite WHERE dateEffective = '2026-03-02 14:00:00';

SELECT * FROM Activite WHERE dureeEstimeeHeures = 3;

SELECT * FROM Activite WHERE idCollaborateur = 3;

SELECT * FROM Activite WHERE statut = 'TERMINEE';

SELECT * FROM Activite WHERE idPrestation = 2;

-- combinaison
SELECT * FROM Activite WHERE statut = 'EN_COURS' AND idCollaborateur = 8;



--  DAOFacture  (src/dao/DAOFacture.py)


-- find_facture : 
SELECT * FROM Facture WHERE numeroFacture = 'FACT-2026-001';

-- select_facture (sans critère)
SELECT * FROM Facture;

-- select_facture 
SELECT * FROM Facture WHERE numeroFacture = 'FACT-2026-001';

SELECT * FROM Facture WHERE dateEmission = '2026-01-15';

SELECT * FROM Facture WHERE montantTotal = 1500.00;

SELECT * FROM Facture WHERE etat = 'PAYEE';

SELECT * FROM Facture WHERE numeroContrat = 'CONT-2026-001';

-- combinaison
SELECT * FROM Facture WHERE etat = 'PAYEE' AND numeroContrat = 'CONT-2026-002';



--  DAOPaiement  (src/dao/DAOPaiement.py)


-- find_paiement : 
SELECT * FROM Paiement WHERE idPaiement = 1;

-- select_paiement (sans critère)
SELECT * FROM Paiement;

-- select_paiement 
SELECT * FROM Paiement WHERE idPaiement = 1;

SELECT * FROM Paiement WHERE datePaiement = '2026-01-26';

SELECT * FROM Paiement WHERE montantPaye = 1500.00;

SELECT * FROM Paiement WHERE numeroFacture = 'FACT-2026-002';

-- combinaison
SELECT * FROM Paiement WHERE numeroFacture = 'FACT-2026-009' AND montantPaye = 1500.00;



--  DAOUtilisateur  (src/dao/DAOUtilisateur.py)


-- authentifier : vérification identifiants (email + mot de passe en clair)
SELECT idUtilisateur, nom, prenom, email, role, statut
FROM Utilisateur
WHERE email = 'admin@comart.fr'
  AND motDePasse = 'hashed_password_1'
  AND statut = 'ACTIF';

-- authentifier_hash : récupère l'enregistrement pour comparaison côté Python
SELECT idUtilisateur, nom, prenom, motDePasse, email, role, statut
FROM Utilisateur
WHERE email = 'admin@comart.fr';

-- get_all_utilisateurs : liste complète
SELECT * FROM Utilisateur;