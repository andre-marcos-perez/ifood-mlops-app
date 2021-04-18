# ----------------------------------------------------------------------------
# - FILE: schema.sql
# - DESC: Create ifood-ml-app database schema.
# ----------------------------------------------------------------------------
# - AUTH: Andre Perez, andre.marcos.perez@gmail.com
# - DATE: 2020-04-16
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# -- SETUP
# ----------------------------------------------------------------------------

DROP SCHEMA IF EXISTS ifood_ml_app_db;
CREATE SCHEMA ifood_ml_app_db;
USE ifood_ml_app_db;

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

# -- EXPERIMENT

CREATE TABLE experiment (
	id INT NOT NULL AUTO_INCREMENT,
	project_id INT NOT NULL,

	engine VARCHAR(30) UNIQUE NOT NULL,
	model_name #varchar
	model_pickle #blob

	data #blob
	hyperparam #json

	



	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_experiment PRIMARY KEY (id),
    FOREIGN KEY (project_id) REFERENCES project (id),
);

# -- TB_STATUS

CREATE TABLE tb_status (
    id INT UNIQUE NOT NULL AUTO_INCREMENT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status_name VARCHAR(30) UNIQUE NOT NULL,
    CONSTRAINT pk_tb_status PRIMARY KEY (id)
);

INSERT INTO tb_status (status_name) VALUES ('RUNNING');
INSERT INTO tb_status (status_name) VALUES ('FINISHED_WITH_SUCCESS');
INSERT INTO tb_status (status_name) VALUES ('FINISHED_WITH_FAILURE');

# -- TB_PROCESS

CREATE TABLE tb_process (
	id INT NOT NULL AUTO_INCREMENT,
	job_id INT NOT NULL,
    status_id INT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT pk_tb_process PRIMARY KEY (id, job_id, status_id),
    FOREIGN KEY (job_id) REFERENCES tb_job (id),
    FOREIGN KEY (status_id) REFERENCES tb_status (id)
);

# ----------------------------------------------------------------------------
# -- ROLLBACK
# ----------------------------------------------------------------------------

# DROP TABLE IF EXISTS tb_process;
# DROP TABLE IF EXISTS tb_status;
# DROP TABLE IF EXISTS tb_job;