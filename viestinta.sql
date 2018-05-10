DROP TABLE IF EXISTS Viestit
;

DROP TABLE IF EXISTS Chat
;

CREATE TABLE Viestit (
ViestiID INTEGER PRIMARY KEY AUTOINCREMENT,
Nimi VARCHAR(50) NOT NULL,
Viesti VARCHAR(100) NOT NULL,
Paiva DATE NOT NULL,
Poisto BOOLEAN NOT NULL,
Deadline DATE
);

INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto) VALUES ('Admin', 'Ensimmainen entry', '2018-05-10', 'FALSE');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto) VALUES ('Admin', 'Toinen entry', '2018-05-10', 'FALSE');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto) VALUES ('Jorma', 'asd', '2018-05-10', 'TRUE');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto) VALUES ('Jarmo', 'fgh', '2018-05-10', 'TRUE');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto) VALUES ('Paavo', 'jkl', '2018-05-10', 'TRUE');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline) VALUES ('Paavo', 'jkl', '2018-05-10', 'TRUE', '2018-05-13');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline) VALUES ('Paavo', 'jkl', '2018-05-10', 'TRUE', '2018-05-12');

CREATE TABLE Chat (
ChatID INTEGER PRIMARY KEY AUTOINCREMENT,
Teksti VARCHAR(50) NOT NULL
);

INSERT INTO Chat (Teksti) VALUES ('Haloo');
INSERT INTO Chat (Teksti) VALUES ('Mitas');
INSERT INTO Chat (Teksti) VALUES ('hoi');
INSERT INTO Chat (Teksti) VALUES ('asdf');
INSERT INTO Chat (Teksti) VALUES ('123123');