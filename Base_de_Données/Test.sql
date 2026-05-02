--- CREATION BASE DE DONNEES
DROP DATABASE IF EXISTS test_comart;
CREATE DATABASE IF NOT EXISTS test_comart;

USE test_comart;

--    CLIENT
CREATE TABLE Client (
    idClient INT AUTO_INCREMENT PRIMARY KEY,
    typeClient ENUM('PARTICULIER', 'ENTREPRISE') NOT NULL,
    nom VARCHAR(100),              -- NULL si entreprise
    prenom VARCHAR(100),           -- NULL si entreprise
    raisonSociale VARCHAR(255),    -- NULL si particulier
    adressePostale VARCHAR(255),
    telephone VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    statut ENUM('PROSPECT', 'CLIENT', 'ANCIEN') NOT NULL,

    -- Contraintes de cohérence selon le type
    CONSTRAINT check_particulier CHECK (
        (typeClient = 'PARTICULIER' AND nom IS NOT NULL AND prenom IS NOT NULL)
        OR
        (typeClient = 'ENTREPRISE' AND raisonSociale IS NOT NULL)
    )
);

--          CONTRAT
CREATE TABLE Contrat (
    numeroContrat VARCHAR(50) PRIMARY KEY,
    dateDebut DATE,
    duree VARCHAR(50),
    nbProductionsTotales INT,
    periodicite ENUM('MENSUELLE', 'ANNUELLE','HEBDOMADAIRE'),
    montantGlobal DECIMAL(10,2),
    conditionsPaiement TEXT,
    idClient int, 
    FOREIGN KEY (idClient) REFERENCES Client(idClient)
);

--           DEVIS
CREATE TABLE Devis (
    numeroDevis VARCHAR(50) PRIMARY KEY,
    dateEmission DATE,
    dateValidite DATE,
    descriptionPrestation TEXT,
    quantitePrevue INT,
    detailsCouts TEXT,
    montantTotalEstime DECIMAL(10,2),
    statut ENUM('EN_ATTENTE', 'ACCEPTE', 'REFUSE', 'EXPIRE'),
    dateAcceptation date,
    idClient INT REFERENCES Client(idClient),
    numeroContrat VARCHAR(50), 
    FOREIGN KEY(numeroContrat) REFERENCES Contrat(numeroContrat),
    CONSTRAINT chk_devis_dates CHECK (dateValidite IS NULL OR dateValidite >= dateEmission),
    
    -- Contraintes de cohérence selon le statut du devis
    CONSTRAINT check_date_acceptation CHECK (
        (statut = 'ACCEPTE' AND dateAcceptation IS NOT NULL)
        OR
        (statut = 'REFUSE' AND dateAcceptation IS  NULL)
        OR
        (statut = 'EN_ATTENTE' AND dateAcceptation IS  NULL)
        OR
        (statut = 'EXPIRE' AND dateAcceptation IS  NULL)
    )
    );

--          FACTURE
CREATE TABLE Facture (
    numeroFacture VARCHAR(50) PRIMARY KEY,
    dateEmission DATE,
    montantTotal DECIMAL(10,2),
    etat ENUM('EN_ATTENTE', 'PAYEE', 'PARTIELLEMENT_PAYEE'),
    numeroContrat VARCHAR(50), 
    FOREIGN KEY(numeroContrat) REFERENCES Contrat(numeroContrat)
);

--          PAIEMENT
CREATE TABLE Paiement (
  idPaiement INT AUTO_INCREMENT PRIMARY KEY,
  datePaiement DATE NOT NULL,
  montantPaye NUMERIC(14,2) NOT NULL CHECK (montantPaye >= 0),
  numeroFacture VARCHAR(50) NOT NULL,
   FOREIGN KEY(numeroFacture) REFERENCES Facture(numeroFacture)

);

--        PRESTATION
CREATE TABLE Prestation (
    idPrestation INT AUTO_INCREMENT PRIMARY KEY,
    datePrevue DATETIME,
    dateEffective DATETIME,
    lieu VARCHAR(255),
    type ENUM('COMM_REGULIERE', 'MARIAGE', 'EVENT_PRO', 'AUTRE'),
    nbPhotosPrevues INT,
    nbVideosPrevues INT,
    numeroContrat VARCHAR(50),
    FOREIGN KEY(numeroContrat) REFERENCES Contrat(numeroContrat),
    CONSTRAINT date_check CHECK (dateEffective IS NULL OR dateEffective >= datePrevue)
);

--         ACTIVITÉ
CREATE TABLE Activite (
    idActivite INT AUTO_INCREMENT PRIMARY KEY,
    libelleOperationnel VARCHAR(255),
    datePrevue DATETIME,
    dateEffective DATETIME,
    dureeEstimeeHeures INT,
    responsable VARCHAR(255),
    statut ENUM('PREVUE', 'EN_COURS', 'TERMINEE'),
    idPrestation INT,
    FOREIGN KEY(idPrestation) REFERENCES Prestation(idPrestation)
);

-- UTILISATEUR (Collaborateurs et Admins)
CREATE TABLE Utilisateur (
    idUtilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    motDePasse VARCHAR(255) NOT NULL,  -- À hasher en production !
    role ENUM('ADMIN', 'COLLABORATEUR') NOT NULL,
    statut ENUM('ACTIF', 'INACTIF') DEFAULT 'ACTIF',
    dateCreation DATETIME DEFAULT CURRENT_TIMESTAMP,
    idCreateur INT,  -- Quel admin a créé ce compte
    FOREIGN KEY(idCreateur) REFERENCES Utilisateur(idUtilisateur)
);

-- Insérer un admin par défaut
INSERT INTO Utilisateur (nom, prenom, email, motDePasse, role) 
VALUES ('Admin', 'Principal', 'root@gmail.com', 'root', 'ADMIN');
INSERT INTO Utilisateur (nom, prenom, email, motDePasse, statut , role) 
VALUES ('Admin2', 'Principal2', 'root2@gmail.com', 'root2', 'INACTIF', 'ADMIN');

-- Insert Temporaire

INSERT INTO Client (typeClient, nom, prenom, raisonSociale, adressePostale, telephone, email, statut)
VALUES
-- Particuliers
('PARTICULIER', 'Descartes', 'René', NULL, 'Panthéon 76000', '0123456789', 'rene.descartes@email.com', 'ANCIEN'),
('PARTICULIER', 'Martin', 'Sophie', NULL, '12 Rue de Rivoli, 75004 Paris', '0612345678', 'sophie.martin@email.com', 'CLIENT'),
('PARTICULIER', 'Dubois', 'Pierre', NULL, '45 Av des Champs, 69000 Lyon', '0478123456', 'pierre.dubois@email.com', 'CLIENT'),
('PARTICULIER', 'Leroy', 'Claire', NULL, '3 Impasse des Fleurs, 33000 Bordeaux', '0556789012', 'claire.leroy@email.com', 'PROSPECT'),
('PARTICULIER', 'Bernard', 'Thomas', NULL, '8 Bd de la République, 13000 Marseille', '0789012345', 'thomas.bernard@email.com', 'ANCIEN'),

-- Entreprises
('ENTREPRISE', NULL, NULL, 'PhotoPro SAS', '22 Rue des Écoles, 59000 Lille', '0320123456', 'contact@photopro.fr', 'CLIENT'),
('ENTREPRISE', NULL, NULL, 'Studio Lumière', '15 Quai de Seine, 75001 Paris', '0145678901', 'info@studio-lumiere.fr', 'PROSPECT'),
('ENTREPRISE', NULL, NULL, 'EventCorp', '7 Rue des Alpes, 74000 Annecy', '0450123456', 'contact@eventcorp.com', 'CLIENT'),
('ENTREPRISE', NULL, NULL, 'Médias & Co', '10 Av de la Gare, 67000 Strasbourg', '0388123456', 'hello@medias-co.fr', 'ANCIEN'),
('ENTREPRISE', NULL, NULL, 'Art & Image', '3 Rue du Commerce, 44000 Nantes', '0240123456', 'contact@art-image.net', 'CLIENT');

-- Contrat :
INSERT INTO Contrat (numeroContrat, dateDebut, duree, nbProductionsTotales, periodicite, montantGlobal, conditionsPaiement, idClient)
VALUES
('CONT-2026-001', '2026-01-01', '12 mois', 12, 'MENSUELLE', 5000.00, 'Paiement en 3 fois', 1),
('CONT-2026-002', '2026-02-15', '6 mois', 6, 'MENSUELLE', 3000.00, 'Paiement comptant', 2),
('CONT-2026-003', '2026-03-01', '24 mois', 24, 'ANNUELLE', 10000.00, 'Paiement en 10 fois', 3),
('CONT-2026-004', '2026-01-10', '3 mois', 3, 'HEBDOMADAIRE', 1500.00, 'Paiement à la livraison', 4),
('CONT-2026-005', '2026-04-01', '12 mois', 12, 'MENSUELLE', 7500.00, 'Paiement en 4 fois', 5),
('CONT-2026-006', '2026-02-20', '9 mois', 9, 'MENSUELLE', 4500.00, 'Paiement en 2 fois', 6),
('CONT-2026-007', '2026-03-15', '1 mois', 1, 'MENSUELLE', 800.00, 'Paiement comptant', 7),
('CONT-2026-008', '2026-01-25', '18 mois', 18, 'ANNUELLE', 9000.00, 'Paiement en 6 fois', 8),
('CONT-2026-009', '2026-05-01', '6 mois', 6, 'MENSUELLE', 2500.00, 'Paiement en 3 fois', 9),
('CONT-2026-010', '2026-02-01', '12 mois', 12, 'MENSUELLE', 6000.00, 'Paiement en 5 fois', 10);

-- Devis : 
INSERT INTO Devis (numeroDevis, dateEmission, dateValidite, descriptionPrestation, quantitePrevue, detailsCouts, montantTotalEstime, statut, dateAcceptation, idClient, numeroContrat)
VALUES
('DEV-2026-001', '2026-01-01', '2026-01-31', 'Prestation de photographie pour événement', 1, 'Détails des coûts estimés', 1500.00, 'EN_ATTENTE', NULL, 1, 'CONT-2026-001'),
('DEV-2026-002', '2026-02-10', '2026-02-28', 'Shooting photo professionnel', 1, 'Inclut retouches et livraison', 2000.00, 'ACCEPTE', '2026-02-12', 2, 'CONT-2026-002'),
('DEV-2026-003', '2026-03-05', '2026-03-20', 'Reportage mariage complet', 1, '2 photographes, 8h de couverture', 3500.00, 'REFUSE', NULL, 3, 'CONT-2026-003'),
('DEV-2026-004', '2026-01-08', '2026-01-22', 'Séance portrait en studio', 1, '10 photos retouchées', 1200.00, 'EN_ATTENTE', NULL, 4, 'CONT-2026-004'),
('DEV-2026-005', '2026-04-01', '2026-04-15', 'Couverture événement corporate', 1, '50 photos, livraison sous 48h', 2800.00, 'ACCEPTE', '2026-04-03', 5, 'CONT-2026-005'),
('DEV-2026-006', '2026-02-18', '2026-03-02', 'Shooting produit e-commerce', 1, '20 produits, fond blanc', 1800.00, 'EXPIRE', NULL, 6, 'CONT-2026-006'),
('DEV-2026-007', '2026-03-10', '2026-03-25', 'Portraits familiaux', 1, 'Séance en extérieur, 15 photos', 900.00, 'ACCEPTE', '2026-03-12', 7, 'CONT-2026-007'),
('DEV-2026-008', '2026-01-20', '2026-02-05', 'Reportage sportif', 1, '100 photos, droits d''usage inclus', 4000.00, 'REFUSE', NULL, 8, 'CONT-2026-008'),
('DEV-2026-009', '2026-05-01', '2026-05-15', 'Mariage intimiste', 1, '6h de couverture, album inclus', 3000.00, 'EN_ATTENTE', NULL, 9, 'CONT-2026-009'),
('DEV-2026-010', '2026-02-01', '2026-02-15', 'Événement d''entreprise', 1, 'Team building, 50 photos', 2200.00, 'ACCEPTE', '2026-02-05', 10, 'CONT-2026-010');

-- Facture :
INSERT INTO Facture (numeroFacture, dateEmission, montantTotal, etat, numeroContrat)
VALUES
('FACT-2026-001', '2026-01-15', 1500.00, 'PAYEE', 'CONT-2026-001'),
('FACT-2026-002', '2026-02-20', 2000.00, 'EN_ATTENTE', 'CONT-2026-002'),
('FACT-2026-003', '2026-03-10', 3500.00, 'PARTIELLEMENT_PAYEE', 'CONT-2026-003'),
('FACT-2026-004', '2026-01-25', 1200.00, 'PAYEE', 'CONT-2026-004'),
('FACT-2026-005', '2026-04-10', 2800.00, 'EN_ATTENTE', 'CONT-2026-005'),
('FACT-2026-006', '2026-03-01', 1800.00, 'PAYEE', 'CONT-2026-006'),
('FACT-2026-007', '2026-03-20', 900.00, 'PARTIELLEMENT_PAYEE', 'CONT-2026-007'),
('FACT-2026-008', '2026-02-05', 4000.00, 'EN_ATTENTE', 'CONT-2026-008'),
('FACT-2026-009', '2026-05-10', 3000.00, 'PAYEE', 'CONT-2026-009'),
('FACT-2026-010', '2026-02-15', 2200.00, 'PARTIELLEMENT_PAYEE', 'CONT-2026-010');


-- Paiement :
INSERT INTO Paiement (datePaiement, montantPaye, numeroFacture)
VALUES
('2026-01-16', 1500.00, 'FACT-2026-001'),  -- Facture entièrement payée
('2026-02-22', 1000.00, 'FACT-2026-002'),  -- Paiement partiel
('2026-03-12', 2000.00, 'FACT-2026-003'),  -- Paiement partiel (3500 - 2000 = 1500 restant)
('2026-01-26', 1200.00, 'FACT-2026-004'),  -- Facture entièrement payée
('2026-04-12', 1400.00, 'FACT-2026-005'),  -- Paiement partiel
('2026-03-02', 1800.00, 'FACT-2026-006'),  -- Facture entièrement payée
('2026-03-22', 500.00, 'FACT-2026-007'),   -- Paiement partiel (900 - 500 = 400 restant)
('2026-02-10', 2000.00, 'FACT-2026-008'),  -- Paiement partiel
('2026-05-12', 3000.00, 'FACT-2026-009'),  -- Facture entièrement payée
('2026-02-20', 1000.00, 'FACT-2026-010'); -- Paiement partiel (2200 - 1000 = 1200 restant)

-- Prestation 
INSERT INTO Prestation (datePrevue, dateEffective, lieu, type, nbPhotosPrevues, nbVideosPrevues, numeroContrat)
VALUES
('2026-02-15 14:00:00', NULL, 'Paris', 'MARIAGE', 100, 5, 'CONT-2026-001'),
('2026-03-01 10:00:00', '2026-03-01 10:00:00', 'Studio Photo Paris', 'COMM_REGULIERE', 50, 0, 'CONT-2026-002'),
('2026-04-10 09:00:00', NULL, 'Château de Versailles', 'MARIAGE', 200, 10, 'CONT-2026-003'),
('2026-01-20 15:00:00', '2026-01-20 15:00:00', 'Studio Lumière', 'COMM_REGULIERE', 10, 0, 'CONT-2026-004'),
('2026-05-15 11:00:00', NULL, 'Palais des Congrès', 'EVENT_PRO', 50, 3, 'CONT-2026-005'),
('2026-03-05 14:00:00', NULL, 'Bureau Client', 'AUTRE', 20, 0, 'CONT-2026-006'),
('2026-03-25 16:00:00', '2026-03-25 16:00:00', 'Parc de la Tête d''Or', 'COMM_REGULIERE', 15, 0, 'CONT-2026-007'),
('2026-02-10 08:00:00', NULL, 'Stade de France', 'EVENT_PRO', 100, 5, 'CONT-2026-008'),
('2026-06-01 12:00:00', NULL, 'Mairie de Strasbourg', 'MARIAGE', 80, 2, 'CONT-2026-009'),
('2026-03-10 13:00:00', '2026-03-10 13:00:00', 'Siège Social', 'EVENT_PRO', 50, 0, 'CONT-2026-010');

-- Activite
INSERT INTO Activite (libelleOperationnel, datePrevue, dateEffective, dureeEstimeeHeures, responsable, statut, idPrestation)
VALUES
('Préparation du matériel', '2026-02-14 10:00:00', NULL, 2, 'Jean Dupont', 'PREVUE', 1),
('Retouches photos', '2026-03-02 14:00:00', '2026-03-02 14:00:00', 3, 'Marie Martin', 'TERMINEE', 2),
('Repérage lieu', '2026-04-09 11:00:00', NULL, 1, 'Luc Bernard', 'PREVUE', 3),
('Installation studio', '2026-01-19 09:00:00', '2026-01-19 09:00:00', 1, 'Sophie Leroy', 'TERMINEE', 4),
('Brief client', '2026-05-14 10:00:00', NULL, 2, 'Pierre Dubois', 'PREVUE', 5),
('Prise de vue produits', '2026-03-04 15:00:00', NULL, 4, 'Antoine Roux', 'EN_COURS', 6),
('Sélection photos', '2026-03-26 10:00:00', '2026-03-26 10:00:00', 2, 'Camille Girard', 'TERMINEE', 7),
('Montage vidéo', '2026-02-11 09:00:00', NULL, 5, 'Thomas Bernard', 'EN_COURS', 8),
('Préparation album', '2026-05-31 14:00:00', NULL, 3, 'Élodie Moreau', 'PREVUE', 9),
('Livraison photos', '2026-03-11 16:00:00', '2026-03-11 16:00:00', 1, 'Julie Lefèvre', 'TERMINEE', 10);

-- Admin 1 (créateur des autres comptes)
INSERT INTO Utilisateur (nom, prenom, email, motDePasse, role, statut, dateCreation, idCreateur)
VALUES ('Admin', 'Root', 'admin@comart.fr', 'hashed_password_1', 'ADMIN', 'ACTIF', '2025-01-01 00:00:00', NULL);

-- Admin 2 (créé par Admin 1)
INSERT INTO Utilisateur (nom, prenom, email, motDePasse, role, statut, dateCreation, idCreateur)
VALUES ('Dupont', 'Jean', 'j.dupont@comart.fr', 'hashed_password_2', 'ADMIN', 'ACTIF', '2025-02-01 00:00:00', 1);

-- Collaborateurs (créés par Admin 1 ou 2)
INSERT INTO Utilisateur (nom, prenom, email, motDePasse, role, statut, dateCreation, idCreateur)
VALUES
('Martin', 'Sophie', 's.martin@comart.fr', 'hashed_password_3', 'COLLABORATEUR', 'ACTIF', '2025-03-01 00:00:00', 1),
('Dubois', 'Pierre', 'p.dubois@comart.fr', 'hashed_password_4', 'COLLABORATEUR', 'ACTIF', '2025-03-15 00:00:00', 2),
('Leroy', 'Claire', 'c.leroy@comart.fr', 'hashed_password_5', 'COLLABORATEUR', 'INACTIF', '2025-04-01 00:00:00', 1),
('Bernard', 'Thomas', 't.bernard@comart.fr', 'hashed_password_6', 'COLLABORATEUR', 'ACTIF', '2025-04-15 00:00:00', 2),
('Moreau', 'Élodie', 'e.moreau@comart.fr', 'hashed_password_7', 'COLLABORATEUR', 'ACTIF', '2025-05-01 00:00:00', 1),
('Fontaine', 'Luc', 'l.fontaine@comart.fr', 'hashed_password_8', 'COLLABORATEUR', 'ACTIF', '2025-05-15 00:00:00', 2),
('Girard', 'Camille', 'c.girard@comart.fr', 'hashed_password_9', 'COLLABORATEUR', 'INACTIF', '2025-06-01 00:00:00', 1),
('Roux', 'Antoine', 'a.roux@comart.fr', 'hashed_password_10', 'COLLABORATEUR', 'ACTIF', '2025-06-15 00:00:00', 2);