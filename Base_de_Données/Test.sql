-- CRÉATION BASE DE DONNÉES : test_comart
DROP DATABASE IF EXISTS test_comart;
CREATE DATABASE IF NOT EXISTS test_comart;
USE test_comart;

CREATE TABLE Client (
    idClient        INT AUTO_INCREMENT PRIMARY KEY,
    typeClient      ENUM('PARTICULIER', 'ENTREPRISE') NOT NULL,
    nom             VARCHAR(100),
    prenom          VARCHAR(100),
    raisonSociale   VARCHAR(255),
    adressePostale  VARCHAR(255),
    telephone       VARCHAR(50),
    email           VARCHAR(255) UNIQUE NOT NULL,
    statut          ENUM('PROSPECT', 'CLIENT', 'ANCIEN') NOT NULL,

    CONSTRAINT check_particulier CHECK (
        (typeClient = 'PARTICULIER' AND nom IS NOT NULL AND prenom IS NOT NULL)
        OR
        (typeClient = 'ENTREPRISE'  AND raisonSociale IS NOT NULL)
    )
);

CREATE TABLE Utilisateur (
    idUtilisateur   INT AUTO_INCREMENT PRIMARY KEY,
    nom             VARCHAR(100)  NOT NULL,
    prenom          VARCHAR(100)  NOT NULL,
    email           VARCHAR(255)  UNIQUE NOT NULL,
    motDePasse      VARCHAR(255)  NOT NULL,
    role            ENUM('ADMIN', 'COLLABORATEUR') NOT NULL,
    statut          ENUM('ACTIF', 'INACTIF') DEFAULT 'ACTIF',
    dateCreation    DATETIME      DEFAULT CURRENT_TIMESTAMP,
    idCreateur      INT,
    FOREIGN KEY (idCreateur) REFERENCES Utilisateur(idUtilisateur)
);

CREATE TABLE Contrat (
    numeroContrat       VARCHAR(50) PRIMARY KEY,
    dateDebut           DATE,
    duree               VARCHAR(50),
    nbProductionsTotales INT,
    periodicite         ENUM('MENSUELLE', 'ANNUELLE', 'HEBDOMADAIRE'),
    montantGlobal       DECIMAL(10,2),
    conditionsPaiement  TEXT,
    idClient            INT,
    FOREIGN KEY (idClient) REFERENCES Client(idClient)
);

CREATE TABLE Devis (
    numeroDevis         VARCHAR(50) PRIMARY KEY,
    dateEmission        DATE,
    dateValidite        DATE,
    descriptionPrestation TEXT,
    quantitePrevue      INT,
    detailsCouts        TEXT,
    montantTotalEstime  DECIMAL(10,2),
    statut              ENUM('EN_ATTENTE', 'ACCEPTE', 'REFUSE', 'EXPIRE'),
    dateAcceptation     DATE,
    idClient            INT,
    numeroContrat       VARCHAR(50),
    FOREIGN KEY (idClient)       REFERENCES Client(idClient),
    FOREIGN KEY (numeroContrat)  REFERENCES Contrat(numeroContrat),

    CONSTRAINT chk_devis_dates CHECK (
        dateValidite IS NULL OR dateValidite >= dateEmission
    ),
    CONSTRAINT check_date_acceptation CHECK (
        (statut = 'ACCEPTE'    AND dateAcceptation IS NOT NULL)
        OR
        (statut IN ('REFUSE', 'EN_ATTENTE', 'EXPIRE') AND dateAcceptation IS NULL)
    )
);

CREATE TABLE Collaborateur (
    idCollaborateur INT AUTO_INCREMENT PRIMARY KEY,
    nom             VARCHAR(100) NOT NULL,
    prenom          VARCHAR(100) NOT NULL,
    poste           VARCHAR(255),
    telephonePro    VARCHAR(50),
    numeroDevis     VARCHAR(50),
    idUtilisateur   INT UNIQUE,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY (numeroDevis)   REFERENCES Devis(numeroDevis)
);

CREATE TABLE Prestation (
    idPrestation    INT AUTO_INCREMENT PRIMARY KEY,
    datePrevue      DATETIME,
    dateEffective   DATETIME,
    lieu            VARCHAR(255),
    type            ENUM('COMM_REGULIERE', 'MARIAGE', 'EVENT_PRO', 'AUTRE'),
    nbPhotosPrevues INT,
    nbVideosPrevues INT,
    numeroContrat   VARCHAR(50),
    FOREIGN KEY (numeroContrat) REFERENCES Contrat(numeroContrat),
    CONSTRAINT date_check CHECK (dateEffective IS NULL OR dateEffective >= datePrevue)
);

CREATE TABLE Activite (
    idActivite          INT AUTO_INCREMENT PRIMARY KEY,
    libelleOperationnel VARCHAR(255),
    datePrevue          DATETIME,
    dateEffective       DATETIME,
    dureeEstimeeHeures  INT,
    statut              ENUM('PREVUE', 'EN_COURS', 'TERMINEE'),
    idCollaborateur     INT,
    idPrestation        INT,
    FOREIGN KEY (idCollaborateur) REFERENCES Collaborateur(idCollaborateur),
    FOREIGN KEY (idPrestation)    REFERENCES Prestation(idPrestation)
);

CREATE TABLE Facture (
    numeroFacture   VARCHAR(50) PRIMARY KEY,
    dateEmission    DATE,
    montantTotal    DECIMAL(10,2),
    etat            ENUM('EN_ATTENTE', 'PAYEE', 'PARTIELLEMENT_PAYEE'),
    numeroContrat   VARCHAR(50),
    FOREIGN KEY (numeroContrat) REFERENCES Contrat(numeroContrat)
);

CREATE TABLE Paiement (
    idPaiement      INT AUTO_INCREMENT PRIMARY KEY,
    datePaiement    DATE            NOT NULL,
    montantPaye     NUMERIC(14,2)   NOT NULL CHECK (montantPaye >= 0),
    numeroFacture   VARCHAR(50)     NOT NULL,
    FOREIGN KEY (numeroFacture) REFERENCES Facture(numeroFacture)
);

-- INSERT INTO 

INSERT INTO Client (typeClient, nom, prenom, raisonSociale, adressePostale, telephone, email, statut) VALUES
('PARTICULIER', 'Descartes', 'René',    NULL,             'Panthéon 76000',                   '0123456789', 'rene.descartes@email.com', 'ANCIEN'),
('PARTICULIER', 'Martin',    'Sophie',  NULL,             '12 Rue de Rivoli, 75004 Paris',     '0612345678', 'sophie.martin@email.com',  'CLIENT'),
('PARTICULIER', 'Dubois',    'Pierre',  NULL,             '45 Av des Champs, 69000 Lyon',      '0478123456', 'pierre.dubois@email.com',  'CLIENT'),
('PARTICULIER', 'Leroy',     'Claire',  NULL,             '3 Impasse des Fleurs, 33000 Bordeaux','0556789012','claire.leroy@email.com',   'PROSPECT'),
('PARTICULIER', 'Bernard',   'Thomas',  NULL,             '8 Bd de la République, 13000 Marseille','0789012345','thomas.bernard@email.com','ANCIEN'),
('ENTREPRISE',  NULL, NULL, 'PhotoPro SAS',               '22 Rue des Écoles, 59000 Lille',    '0320123456', 'contact@photopro.fr',      'CLIENT'),
('ENTREPRISE',  NULL, NULL, 'Studio Lumière',             '15 Quai de Seine, 75001 Paris',     '0145678901', 'info@studio-lumiere.fr',   'PROSPECT'),
('ENTREPRISE',  NULL, NULL, 'EventCorp',                  '7 Rue des Alpes, 74000 Annecy',     '0450123456', 'contact@eventcorp.com',    'CLIENT'),
('ENTREPRISE',  NULL, NULL, 'Médias & Co',                '10 Av de la Gare, 67000 Strasbourg','0388123456', 'hello@medias-co.fr',       'ANCIEN'),
('ENTREPRISE',  NULL, NULL, 'Art & Image',                '3 Rue du Commerce, 44000 Nantes',   '0240123456', 'contact@art-image.net',    'CLIENT');


INSERT INTO Utilisateur (idUtilisateur, nom, prenom, email, motDePasse, role, statut, dateCreation, idCreateur) VALUES
(1,  'Admin',    'Root',    'admin@comart.fr',     'hashed_password_1',  'ADMIN',          'ACTIF',   '2025-01-01 00:00:00', NULL),
(2,  'Dupont',   'Jean',    'j.dupont@comart.fr',  'hashed_password_2',  'ADMIN',          'ACTIF',   '2025-02-01 00:00:00', 1),
(3,  'Martin',   'Sophie',  's.martin@comart.fr',  'hashed_password_3',  'COLLABORATEUR',  'ACTIF',   '2025-03-01 00:00:00', 1),
(4,  'Dubois',   'Pierre',  'p.dubois@comart.fr',  'hashed_password_4',  'COLLABORATEUR',  'ACTIF',   '2025-03-15 00:00:00', 2),
(5,  'Leroy',    'Claire',  'c.leroy@comart.fr',   'hashed_password_5',  'COLLABORATEUR',  'INACTIF', '2025-04-01 00:00:00', 1),
(6,  'Bernard',  'Thomas',  't.bernard@comart.fr', 'hashed_password_6',  'COLLABORATEUR',  'ACTIF',   '2025-04-15 00:00:00', 2),
(7,  'Moreau',   'Élodie',  'e.moreau@comart.fr',  'hashed_password_7',  'COLLABORATEUR',  'ACTIF',   '2025-05-01 00:00:00', 1),
(8,  'Fontaine', 'Luc',     'l.fontaine@comart.fr','hashed_password_8',  'COLLABORATEUR',  'ACTIF',   '2025-05-15 00:00:00', 2),
(9,  'Girard',   'Camille', 'c.girard@comart.fr',  'hashed_password_9',  'COLLABORATEUR',  'INACTIF', '2025-06-01 00:00:00', 1),
(10, 'Roux',     'Antoine', 'a.roux@comart.fr',    'hashed_password_10', 'COLLABORATEUR',  'ACTIF',   '2025-06-15 00:00:00', 2),
(11,  'root',    'root',    'root@comart.fr',      'root',               'ADMIN',          'ACTIF',   '2025-02-01 00:00:00', 1);


INSERT INTO Contrat (numeroContrat, dateDebut, duree, nbProductionsTotales, periodicite, montantGlobal, conditionsPaiement, idClient) VALUES
('CONT-2026-001', '2026-01-01', '12 mois',  12, 'MENSUELLE',    5000.00,  'Paiement en 3 fois',         1),
('CONT-2026-002', '2026-02-15', '6 mois',    6, 'MENSUELLE',    3000.00,  'Paiement comptant',          2),
('CONT-2026-003', '2026-03-01', '24 mois',  24, 'ANNUELLE',    10000.00,  'Paiement en 10 fois',        3),
('CONT-2026-004', '2026-01-10', '3 mois',    3, 'HEBDOMADAIRE', 1500.00,  'Paiement à la livraison',    4),
('CONT-2026-005', '2026-04-01', '12 mois',  12, 'MENSUELLE',    7500.00,  'Paiement en 4 fois',         5),
('CONT-2026-006', '2026-02-20', '9 mois',    9, 'MENSUELLE',    4500.00,  'Paiement en 2 fois',         6),
('CONT-2026-007', '2026-03-15', '1 mois',    1, 'MENSUELLE',     800.00,  'Paiement comptant',          7),
('CONT-2026-008', '2026-01-25', '18 mois',  18, 'ANNUELLE',     9000.00,  'Paiement en 6 fois',         8),
('CONT-2026-009', '2026-05-01', '6 mois',    6, 'MENSUELLE',    2500.00,  'Paiement en 3 fois',         9),
('CONT-2026-010', '2026-02-01', '12 mois',  12, 'MENSUELLE',    6000.00,  'Paiement en 5 fois',        10);


INSERT INTO Devis (numeroDevis, dateEmission, dateValidite, descriptionPrestation, quantitePrevue, detailsCouts, montantTotalEstime, statut, dateAcceptation, idClient, numeroContrat) VALUES
('DEV-2026-001', '2026-01-01', '2026-01-31', 'Prestation de photographie pour événement', 1, 'Détails des coûts estimés',             1500.00, 'EN_ATTENTE', NULL,         1, 'CONT-2026-001'),
('DEV-2026-002', '2026-02-10', '2026-02-28', 'Shooting photo professionnel',              1, 'Inclut retouches et livraison',         2000.00, 'ACCEPTE',    '2026-02-12', 2, 'CONT-2026-002'),
('DEV-2026-003', '2026-03-05', '2026-03-20', 'Reportage mariage complet',                 1, '2 photographes, 8h de couverture',     3500.00, 'REFUSE',     NULL,         3, 'CONT-2026-003'),
('DEV-2026-004', '2026-01-08', '2026-01-22', 'Séance portrait en studio',                 1, '10 photos retouchées',                 1200.00, 'EN_ATTENTE', NULL,         4, 'CONT-2026-004'),
('DEV-2026-005', '2026-04-01', '2026-04-15', 'Couverture événement corporate',            1, '50 photos, livraison sous 48h',        2800.00, 'ACCEPTE',    '2026-04-03', 5, 'CONT-2026-005'),
('DEV-2026-006', '2026-02-18', '2026-03-02', 'Shooting produit e-commerce',               1, '20 produits, fond blanc',              1800.00, 'EXPIRE',     NULL,         6, 'CONT-2026-006'),
('DEV-2026-007', '2026-03-10', '2026-03-25', 'Portraits familiaux',                       1, 'Séance en extérieur, 15 photos',        900.00, 'ACCEPTE',    '2026-03-12', 7, 'CONT-2026-007'),
('DEV-2026-008', '2026-01-20', '2026-02-05', 'Reportage sportif',                         1, '100 photos, droits d''usage inclus',   4000.00, 'REFUSE',     NULL,         8, 'CONT-2026-008'),
('DEV-2026-009', '2026-05-01', '2026-05-15', 'Mariage intimiste',                         1, '6h de couverture, album inclus',       3000.00, 'EN_ATTENTE', NULL,         9, 'CONT-2026-009'),
('DEV-2026-010', '2026-02-01', '2026-02-15', 'Événement d''entreprise',                   1, 'Team building, 50 photos',             2200.00, 'ACCEPTE',    '2026-02-05',10, 'CONT-2026-010');

INSERT INTO Collaborateur (idCollaborateur, nom, prenom, poste, telephonePro, numeroDevis, idUtilisateur) VALUES
(1, 'Martin',   'Sophie',  'Photographe Senior',  '0601010101', NULL,           3),
(2, 'Dubois',   'Pierre',  'Responsable Vidéo',   '0602020202', 'DEV-2026-001', 4),
(3, 'Leroy',    'Claire',  'Retoucheuse Photo',   '0603030303', NULL,           5),
(4, 'Bernard',  'Thomas',  'Commercial Terrain',  '0604040404', 'DEV-2026-002', 6),
(5, 'Moreau',   'Élodie',  'Chef de projet',      '0605050505', NULL,           7),
(6, 'Fontaine', 'Luc',     'Assistant Plateau',   '0606060606', NULL,           8),
(7, 'Girard',   'Camille', 'Community Manager',   '0607070707', NULL,           9),
(8, 'Roux',     'Antoine', 'Vidéaste Junior',     '0608080808', NULL,          10);

INSERT INTO Facture (numeroFacture, dateEmission, montantTotal, etat, numeroContrat) VALUES
('FACT-2026-001', '2026-01-15', 1500.00, 'PAYEE',               'CONT-2026-001'),
('FACT-2026-002', '2026-02-20', 2000.00, 'EN_ATTENTE',          'CONT-2026-002'),
('FACT-2026-003', '2026-03-10', 3500.00, 'PARTIELLEMENT_PAYEE', 'CONT-2026-003'),
('FACT-2026-004', '2026-01-25', 1200.00, 'PAYEE',               'CONT-2026-004'),
('FACT-2026-005', '2026-04-10', 2800.00, 'EN_ATTENTE',          'CONT-2026-005'),
('FACT-2026-006', '2026-03-01', 1800.00, 'PAYEE',               'CONT-2026-006'),
('FACT-2026-007', '2026-03-20',  900.00, 'PARTIELLEMENT_PAYEE', 'CONT-2026-007'),
('FACT-2026-008', '2026-02-05', 4000.00, 'EN_ATTENTE',          'CONT-2026-008'),
('FACT-2026-009', '2026-05-10', 3000.00, 'PAYEE',               'CONT-2026-009'),
('FACT-2026-010', '2026-02-15', 2200.00, 'PARTIELLEMENT_PAYEE', 'CONT-2026-010');

INSERT INTO Paiement (datePaiement, montantPaye, numeroFacture) VALUES
('2026-01-16', 1500.00, 'FACT-2026-001'),
('2026-02-22', 1000.00, 'FACT-2026-002'),
('2026-03-12', 2000.00, 'FACT-2026-003'),
('2026-01-26', 1200.00, 'FACT-2026-004'),
('2026-04-12', 1400.00, 'FACT-2026-005'),
('2026-03-02', 1800.00, 'FACT-2026-006'),
('2026-03-22',  500.00, 'FACT-2026-007'),
('2026-02-10', 2000.00, 'FACT-2026-008'),
('2026-05-12', 3000.00, 'FACT-2026-009'),
('2026-02-20', 1000.00, 'FACT-2026-010');

INSERT INTO Prestation (datePrevue, dateEffective, lieu, type, nbPhotosPrevues, nbVideosPrevues, numeroContrat) VALUES
('2026-02-15 14:00:00', NULL,                    'Paris',                    'MARIAGE',        100, 5,  'CONT-2026-001'),
('2026-03-01 10:00:00', '2026-03-01 10:00:00',   'Studio Photo Paris',       'COMM_REGULIERE',  50, 0,  'CONT-2026-002'),
('2026-04-10 09:00:00', NULL,                    'Château de Versailles',    'MARIAGE',        200, 10, 'CONT-2026-003'),
('2026-01-20 15:00:00', '2026-01-20 15:00:00',   'Studio Lumière',           'COMM_REGULIERE',  10, 0,  'CONT-2026-004'),
('2026-05-15 11:00:00', NULL,                    'Palais des Congrès',       'EVENT_PRO',       50, 3,  'CONT-2026-005'),
('2026-03-05 14:00:00', NULL,                    'Bureau Client',            'AUTRE',           20, 0,  'CONT-2026-006'),
('2026-03-25 16:00:00', '2026-03-25 16:00:00',   'Parc de la Tête d''Or',   'COMM_REGULIERE',  15, 0,  'CONT-2026-007'),
('2026-02-10 08:00:00', NULL,                    'Stade de France',          'EVENT_PRO',      100, 5,  'CONT-2026-008'),
('2026-06-01 12:00:00', NULL,                    'Mairie de Strasbourg',     'MARIAGE',         80, 2,  'CONT-2026-009'),
('2026-03-10 13:00:00', '2026-03-10 13:00:00',   'Siège Social',             'EVENT_PRO',       50, 0,  'CONT-2026-010');


INSERT INTO Activite (libelleOperationnel, datePrevue, dateEffective, dureeEstimeeHeures, statut, idCollaborateur, idPrestation) VALUES
('Préparation du matériel', '2026-02-14 10:00:00', NULL,                    2, 'PREVUE',   1, 1),  -- Sophie Martin
('Retouches photos',        '2026-03-02 14:00:00', '2026-03-02 14:00:00',   3, 'TERMINEE', 3, 2),  -- Claire Leroy
('Repérage lieu',           '2026-04-09 11:00:00', NULL,                    1, 'PREVUE',   6, 3),  -- Luc Fontaine
('Installation studio',     '2026-01-19 09:00:00', '2026-01-19 09:00:00',   1, 'TERMINEE', 1, 4),  -- Sophie Martin
('Brief client',            '2026-05-14 10:00:00', NULL,                    2, 'PREVUE',   2, 5),  -- Pierre Dubois
('Prise de vue produits',   '2026-03-04 15:00:00', NULL,                    4, 'EN_COURS', 8, 6),  -- Antoine Roux
('Sélection photos',        '2026-03-26 10:00:00', '2026-03-26 10:00:00',   2, 'TERMINEE', 7, 7),  -- Camille Girard
('Montage vidéo',           '2026-02-11 09:00:00', NULL,                    5, 'EN_COURS', 4, 8),  -- Thomas Bernard
('Préparation album',       '2026-05-31 14:00:00', NULL,                    3, 'PREVUE',   5, 9),  -- Élodie Moreau
('Livraison photos',        '2026-03-11 16:00:00', '2026-03-11 16:00:00',   1, 'TERMINEE', 3, 10); -- Claire Leroy