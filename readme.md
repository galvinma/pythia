### Setting up Python on OSX. Use Homebrew, PIP, and finally virtualenv.

http://docs.python-guide.org/en/latest/starting/install/osx/

### Video for setting up Flask

https://www.youtube.com/watch?v=DIcpEg77gdE


### Virtualenv (postactive):

#!/bin/bash
# This hook is sourced after this virtualenv is activated.

export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://localhost/pythia"

pythia=$(basename $VIRTUAL_ENV)
cd ~/workspace/pythia

PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"

# For Postgres integration:

http://newcoder.io/scrape/part-4/
http://www.blog.pythonlibrary.org/2012/07/01/a-simple-sqlalchemy-0-7-0-8-tutorial/
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database