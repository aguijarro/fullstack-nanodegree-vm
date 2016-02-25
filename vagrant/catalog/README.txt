description
-----------

instructions to install, configure, and to run the program
------------------------------------------------------------

To execute this app you must do the following steps:

1) Install Requirements:
Go to /vagrant/catalog directory and then execute:  pip install -r requirements.txt


2) Create a database
Open a PostgreSQL terminal and execute the command below:

DROP DATABASE IF EXISTS catalog_dev;
CREATE DATABASE catalog_dev;
\c catalog_dev;

3) In psql terminal, change user password for database to use in connection string
ALTER USER vagrant WITH PASSWORD 'vagrant';

4) In /vagrant/catalog directory open config.py and verify that the string below is configured with the credentials below.
If you don't want to change the original credentials, ensure that the line below contains the right credentials according with your configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://vagrant:vagrant@localhost/catalog_dev'

5) Create a migration repository
In /vagrant/catalog directory execute python app.py db init


6) Create creates database tables
In /vagrant/catalog directory execute python app.py deploy

7) Run server
In /vagrant/catalog directory execute python app.py runserver

8) Go to browser and write: http://localhost:8000/
