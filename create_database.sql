-- =====================================================
-- Braintraining - Database creation script (MySQL 8.0)
-- Authors: Rinit, Arda, Alessio
-- =====================================================

DROP DATABASE IF EXISTS braintraining;
CREATE DATABASE braintraining
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE braintraining;

-- -----------------------------------------------------
-- Table users
-- password_hash and level are used from sprint 3 (login)
-- level: 1 = student, 2 = teacher
-- -----------------------------------------------------
CREATE TABLE users (
    id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username      VARCHAR(50)  NOT NULL,
    password_hash VARCHAR(255) NULL,
    level         TINYINT UNSIGNED NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    CONSTRAINT chk_users_level CHECK (level IN (1, 2))
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table exercises
-- code: exercise identifier used in the program (ex: GEO01)
-- -----------------------------------------------------
CREATE TABLE exercises (
    id   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    code VARCHAR(10)  NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_exercises_code (code)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table results
-- duration: in seconds (ex: 2:07 -> 127), easier to sum for totals
-- -----------------------------------------------------
CREATE TABLE results (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    date_hour   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    duration    INT UNSIGNED NOT NULL,
    nb_trials   INT UNSIGNED NOT NULL,
    nb_ok       INT UNSIGNED NOT NULL,
    user_id     INT UNSIGNED NOT NULL,
    exercise_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT chk_results_ok CHECK (nb_ok <= nb_trials),
    CONSTRAINT fk_results_users
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_results_exercises
        FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Exercises available in the program
-- -----------------------------------------------------
INSERT INTO exercises (code, name) VALUES
    ('GEO01',  'Exercice de géométrie'),
    ('INFO02', 'Conversion d''unités'),
    ('INFO05', 'La couleur perdue');