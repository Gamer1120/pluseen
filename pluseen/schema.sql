DROP TABLE IF EXISTS pluseendeelnemers;
DROP TABLE IF EXISTS deelnemers;
DROP TABLE IF EXISTS pluseens;

CREATE TABLE pluseens
(
    id          SERIAL NOT NULL PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE deelnemers
(
    id   SERIAL NOT NULL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
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
    pluseen_id   INT NOT NULL REFERENCES pluseens (id) ON DELETE CASCADE,
    deelnemer_id INT NOT NULL REFERENCES deelnemers (id) ON DELETE CASCADE,
    status       INT NOT NULL,
    comment      TEXT,
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (pluseen_id, deelnemer_id)
);
