###Board###
* https://trello.com/b/dOa48WoC/pythia

###Virtual Environments and Requirements.txt###

* http://docs.python-guide.org/en/latest/dev/virtualenvs/

Use Pip to install requirements.txt

####Example Commands####

* mkvirtualenv pythia -a /home/galvinma/Workspace/pythia/
* pip install -r /path/to/requirements.txt
* To install psycog2: sudo apt install libpq-dev python-dev

### Postgres Integration ###

Fresh install for a linux user. local_user_account is the current OS account.
* sudo apt-get install postgresql postgresql-contrib 
* sudo service postgresql start
* sudo su - postgres 
* psql
* CREATE USER admin;
* ALTER ROLE admin WITH PASSWORD 'password';
* ALTER ROLE admin WITH SUPERUSER;
* CREATE USER local_user_account;
* ALTER ROLE local_user_account WITH PASSWORD 'password';
* ALTER ROLE local_user_account WITH SUPERUSER;
* CREATE DATABASE pythia;

####Query Postgres####

pythia=# SELECT * FROM "SignUp";

 username | firstname | lastname |         email          | password 
----------+-----------+----------+------------------------+----------
 galvinma | Matthew   | Galvin   | mattgalvin47@gmail.com | password
 dsnfjkas | matthew   | dfsnjks  | dnjkfsa`dnbkdfs`       | ds nfks
(2 rows)

####Creating a Table####

CREATE TABLE "Message"(
   mes_identity TEXT PRIMARY KEY     NOT NULL,
   message           TEXT    NOT NULL
);

####Inserting data into a table####

INSERT INTO "UserConversations"(user_id,conversations_id)                                                                                                               
VALUES (1,1);


####Entering pythia####

workon pythia
psql pythia
\d

####Dropping Schema####

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

then


GRANT USAGE ON SCHEMA public TO public;
GRANT CREATE ON SCHEMA public TO public;

###git###

* http://rogerdudler.github.io/git-guide/
* http://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html

Useful Commands:

* git init
* git clone /path/path/path
* git remote add origin <server>
* git pull origin master
* git push origin master
* git checkout -b <branch_name>
* git checkout master
* git status
* git branch
* git add .
* git commit -m "message"
* git merge <branch>
* git branch -d local_branch
* git branch -d branch_name   (for local delete)
* git push origin --delete remote_branch}   (for remote delete)

Example of merging a branch:

1. git checkout -b <branch_name>
1. Make code changes.
1. git status
1. git add .
1. git commit -m "message"
1. git push <branch_name>
1. git checkout master
1. git pull origin master
1. git merge <branch_name>
1. git push origin master
1. git branch -d <branch_name>
1. git push origin --delete <remote_branch>