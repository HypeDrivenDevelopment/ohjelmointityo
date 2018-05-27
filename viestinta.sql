DROP TABLE IF EXISTS Viestit
;

DROP TABLE IF EXISTS Chat
;

DROP TABLE IF EXISTS Oikeudet
;

DROP TABLE IF EXISTS Motd
;

CREATE TABLE Viestit (
ViestiID INTEGER PRIMARY KEY AUTOINCREMENT,
Nimi VARCHAR(50) NOT NULL,
Viesti VARCHAR(100) NOT NULL,
Paiva DATE NOT NULL,
Poisto BOOLEAN NOT NULL,
Deadline DATE,
Lisatiedot VARCHAR(100)
);

INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline, Lisatiedot) VALUES ('Admin', 'Ensimmainen entry', '2018-05-27', 'FALSE', '', 'jotain');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline, Lisatiedot) VALUES ('Admin', 'Toinen entry', '2018-05-27', 'FALSE', '', 'jotain2');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline, Lisatiedot) VALUES ('Pekka', 'Kolmas entry', '2018-05-27', 'FALSE', '', 'jotain3');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline, Lisatiedot) VALUES ('Pekka', 'Lorem ipsum dolor', '2018-05-27', 'FALSE', '', 'sit amet');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline, Lisatiedot) VALUES ('Admin', 'consectetur adipiscing', '2018-05-27', 'FALSE', '', 'elit, sed do eiusmod tempor');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline, Lisatiedot) VALUES ('Pekka', 'incididunt ut labore', '2018-05-27', 'TRUE', '2018-05-31', '');
INSERT INTO Viestit (Nimi, Viesti, Paiva, Poisto, Deadline, Lisatiedot) VALUES ('Admin', 'et dolore magna aliqua', '2018-05-27', 'TRUE', '2018-05-30', 'Ut enim ad');

CREATE TABLE Chat (
ChatID INTEGER PRIMARY KEY AUTOINCREMENT,
Teksti VARCHAR(50) NOT NULL,
Kayttaja VARCHAR(50) NOT NULL
);

INSERT INTO Chat (Teksti, Kayttaja) VALUES ('Haloo', 'Admin');
INSERT INTO Chat (Teksti, Kayttaja) VALUES ('Terve', 'Pekka');
INSERT INTO Chat (Teksti, Kayttaja) VALUES ('asdf', 'Admin');
INSERT INTO Chat (Teksti, Kayttaja) VALUES ('asdf', 'Admin');
INSERT INTO Chat (Teksti, Kayttaja) VALUES ('123123', 'Pekka');

CREATE TABLE Oikeudet (
OikeusID INTEGER PRIMARY KEY AUTOINCREMENT,
Merkkijono VARCHAR(100) NOT NULL,
Oikeus VARCHAR(10) NOT NULL
);

INSERT INTO Oikeudet (Merkkijono, Oikeus) VALUES ('6416068d531d179b8de9bcab314dbb4788f4280d', 'Admin');
INSERT INTO Oikeudet (Merkkijono, Oikeus) VALUES ('831541fd9aa6c3a4fc73241eb9f62eaba34c889b', 'User');

CREATE TABLE Motd (
ViestiID INTEGER PRIMARY KEY AUTOINCREMENT,
Viesti VARCHAR(100) NOT NULL
);

INSERT INTO Motd (Viesti) VALUES ('Tervehdys');