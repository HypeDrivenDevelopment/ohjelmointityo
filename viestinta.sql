DROP TABLE IF EXISTS Viestit
;

DROP TABLE IF EXISTS Chat
;

CREATE TABLE Viestit (
ViestiID INTEGER PRIMARY KEY AUTOINCREMENT,
Nimi VARCHAR(50) NOT NULL,
Viesti VARCHAR(100) NOT NULL
);

INSERT INTO Viestit (Nimi, Viesti) VALUES ('Admin', 'Ensimmainen entry');
INSERT INTO Viestit (Nimi, Viesti) VALUES ('Admin', 'Toinen entry');
INSERT INTO Viestit (Nimi, Viesti) VALUES ('Jorma', 'asd');
INSERT INTO Viestit (Nimi, Viesti) VALUES ('Jarmo', 'fgh');
INSERT INTO Viestit (Nimi, Viesti) VALUES ('Paavo', 'jkl');

CREATE TABLE Chat (
ChatID INTEGER PRIMARY KEY AUTOINCREMENT,
Teksti VARCHAR(50) NOT NULL
);

INSERT INTO Chat (Teksti) VALUES ('Haloo');
INSERT INTO Chat (Teksti) VALUES ('Mitas');
INSERT INTO Chat (Teksti) VALUES ('hoi');
INSERT INTO Chat (Teksti) VALUES ('asdf');
INSERT INTO Chat (Teksti) VALUES ('123123');