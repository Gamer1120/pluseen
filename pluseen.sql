CREATE TABLE pluseendeelnemers (
pluseenid INT,
deelnemer VARCHAR(255)
);
CREATE TABLE pluseens (
id SERIAL,
name VARCHAR(255)
);
INSERT INTO pluseens(name) VALUES ('test123');
INSERT INTO pluseendeelnemers (pluseenid, deelnemer) VALUES (1, 'Michael');
INSERT INTO pluseendeelnemers (pluseenid, deelnemer) VALUES (1, 'Sven');