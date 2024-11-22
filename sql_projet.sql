DROP TABLE IF EXISTS etudiant;
DROP TABLE IF EXISTS type_marche;
DROP TABLE IF EXISTS lieu;
DROP TABLE IF EXISTS jour_semaine;

CREATE TABLE jour_semaine(
                             id_jour INT AUTO_INCREMENT,
                             libelle_jour VARCHAR(50),
                             PRIMARY KEY(id_jour)
);

CREATE TABLE lieu(
                     id_lieu INT AUTO_INCREMENT,
                     Libelle_lieu VARCHAR(50),
                     PRIMARY KEY(id_lieu)
);

CREATE TABLE type_marche(
                            id_type_marché INT AUTO_INCREMENT,
                            Libelle_type_marché VARCHAR(50),
                            id_lieu INT NOT NULL,
                            nombre_place INT,
                            surface DECIMAL (10,2),
                            PRIMARY KEY(id_type_marché),
                            FOREIGN KEY(id_lieu) REFERENCES lieu(id_lieu)
);

CREATE TABLE etudiant (
id_etudiant INT AUTO_INCREMENT
, nom_etudiant VARCHAR(255)
, groupe_etudiant VARCHAR(255)
, PRIMARY KEY(id_etudiant)
);

INSERT INTO etudiant (id_etudiant, nom_etudiant, groupe_etudiant)
VALUES
(NULL, 'tom','A1'),
(NULL, 'enzo','A1'),
(NULL, 'laurence','A2'),
(NULL, 'theo','A2'),
(NULL, 'theo','B1')
;

SELECT id_etudiant AS id, nom_etudiant AS nom, groupe_etudiant AS groupe
FROM etudiant
ORDER BY nom;

INSERT INTO etudiant(id_etudiant, nom_etudiant, groupe_etudiant) VALUES (NULL, 'test1', 'test1');

DELETE FROM etudiant WHERE id_etudiant=2;

UPDATE etudiant SET nom_etudiant = 'test2', groupe_etudiant= 'test3' WHERE id_etudiant=3;

