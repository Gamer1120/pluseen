DROP TABLE IF EXISTS pluseendeelnemers;
DROP TABLE IF EXISTS deelnemers;
DROP TABLE IF EXISTS pluseens;

CREATE TABLE pluseens
(
    id   SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE deelnemers
(
    id   SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);
INSERT INTO deelnemers (name)
VALUES ('Anne'),
       ('Hans'),
       ('Joaz'),
       ('Joël'),
       ('Lindsay'),
       ('Michael'),
       ('Michelle'),
       ('Pim'),
       ('René'),
       ('Sven');

CREATE TABLE pluseendeelnemers
(
    pluseen_id   INT,
    deelnemer_id INT,
    status       INT,
    PRIMARY KEY (pluseen_id, deelnemer_id),
    FOREIGN KEY (pluseen_id) REFERENCES pluseens (id) ON DELETE CASCADE,
    FOREIGN KEY (deelnemer_id) REFERENCES deelnemers (id) ON DELETE CASCADE
);
