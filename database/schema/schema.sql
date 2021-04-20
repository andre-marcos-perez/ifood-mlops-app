# ----------------------------------------------------------------------------
# - FILE: schema.sql
# - DESC: Create ifood-mlops-app database schema.
# ----------------------------------------------------------------------------
# - AUTH: Andre Perez, andre.marcos.perez@gmail.com
# - DATE: 2020-04-16
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# -- SETUP
# ----------------------------------------------------------------------------

DROP SCHEMA IF EXISTS ifood_mlops_app_db;
CREATE SCHEMA ifood_mlops_app_db;
USE ifood_mlops_app_db;

# ----------------------------------------------------------------------------
# -- MAIN
# ----------------------------------------------------------------------------

# -- PROJECT

CREATE TABLE project (
    id INT UNIQUE NOT NULL AUTO_INCREMENT,
    name VARCHAR(30) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_project PRIMARY KEY (id)
);

CREATE TABLE experiment (
    id INT UNIQUE NOT NULL AUTO_INCREMENT,
    project_id INT NOT NULL,
    engine VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'created',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_experiment PRIMARY KEY (id),
    FOREIGN KEY (project_id) REFERENCES project (id)
);

# ----------------------------------------------------------------------------
# -- ROLLBACK
# ----------------------------------------------------------------------------

# DROP TABLE IF EXISTS experiment;
# DROP TABLE IF EXISTS project;