CREATE TABLE personnage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    nationality TEXT NOT NULL,
    long_bio TEXT NOT NULL,
    short_description NOT NULL,
    birthdate,
    deathdate,
    pictureUrl,
    father,
    mother,
    website
);

CREATE TABLE oeuvre(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_oeuvre TEXT NOT NULL,
    icone NOT NULL
);

CREATE TABLE activite(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_activite NOT NULL
);

CREATE TABLE oeuvre_personnage(
    oeuvreID INTEGER NOT NULL REFERENCES oeuvre(id),
    personnageID INTEGER NOT NULL REFERENCES personnage(id)
);

CREATE TABLE activite_personnage(
    activiteID INTEGER Not NULL REFERENCES activitie(id),
    personnageID INTEGER NOT NULL REFERENCES personnage(id)
);