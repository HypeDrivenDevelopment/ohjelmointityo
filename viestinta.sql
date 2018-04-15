DROP TABLE IF EXISTS Viestit
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
