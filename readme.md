##
##### Setting up Python on OSX. Use Homebrew, PIP, and finally virtualenv. ######
##

http://docs.python-guide.org/en/latest/starting/install/osx/



##
##### Video for setting up Flask ######
##
https://www.youtube.com/watch?v=DIcpEg77gdE



##
##### Virtualenv (postactive) #####
##


export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/pythia"

pythia=$(basename $VIRTUAL_ENV)
cd ~/workspace/pythia

PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"



##
##### For Postgres (9.4.4) integration #####
##

http://newcoder.io/scrape/part-4/
http://www.blog.pythonlibrary.org/2012/07/01/a-simple-sqlalchemy-0-7-0-8-tutorial/
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
http://www.blog.pythonlibrary.org/2010/02/03/another-step-by-step-sqlalchemy-tutorial-part-2-of-2/



##
##### Free Scrum tools #####
##
https://scrumy.com/pythia_scrum_board
https://trello.com/



## 
##### Query Postgres
##

GALVIN-# \l


GALVIN-# \connect pythia

                      
pythia=# SELECT * FROM "SignUp";

 username | firstname | lastname |         email          | password 
----------+-----------+----------+------------------------+----------
 galvinma | Matthew   | Galvin   | mattgalvin47@gmail.com | password
 dsnfjkas | matthew   | dfsnjks  | dnjkfsa`dnbkdfs`       | ds nfks
(2 rows)

