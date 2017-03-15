## Board ##
* https://scrumy.com/pythia_scrum_board

##Virtual Environments and Requirements.txt##

* http://docs.python-guide.org/en/latest/dev/virtualenvs/

Use Pip to install requirements.txt

Example Commands
* mkvirtualenv pythia -a /home/galvinma/Workspace/pythia/
* pip install -r /path/to/requirements.txt
* To install psycog2: sudo apt install libpq-dev python-dev

## Postgres Integration ##

* https://www.cyberciti.biz/faq/howto-add-postgresql-user-account/
* http://newcoder.io/scrape/part-4/  
* http://www.blog.pythonlibrary.org/2012/07/01/a-simple-sqlalchemy-0-7-0-8-tutorial/ 
* http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
* http://www.blog.pythonlibrary.org/2010/02/03/another-step-by-step-sqlalchemy-tutorial-part-2-of-2/

Query Postgres:

GALVIN-# \l
GALVIN-# \connect pythia                 
pythia=# SELECT * FROM "SignUp";

 username | firstname | lastname |         email          | password 
----------+-----------+----------+------------------------+----------
 galvinma | Matthew   | Galvin   | mattgalvin47@gmail.com | password
 dsnfjkas | matthew   | dfsnjks  | dnjkfsa`dnbkdfs`       | ds nfks
(2 rows)


##git##

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