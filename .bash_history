dir
sudo apt-get update
sudo apt-get install git postgresql-12 postgresql-server-dev-12 python3-virtualenv python3-dev
sudo apt update
sudo apt -y install vim bash-completion wget
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt -y install postgresql-12 postgresql-client-12
systemctl status postgresql.service
sudo su - postgres
sudo apt install python3-pip
sudo pip3 install virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
dir
mkvirtualenv dbproj
source .virtualenvs/dbproj/bin/activate
pip3 install psycopg2
sudo apt-get install libpq-dev
pip3 install psycopg2
pip3 install sqlalchemy click
pip3 install flask
deactivate
dir
cd dbproj
python3
source .virtualenvs/dbproj/bin/activate
pip3 install sqlalchemy
pip3 install click
pip3 install psycopg2
deactivate
python
python3
source .virtualenvs/dbproj/bin/activate
pip3 install psycopg2
pip3 install sqlalchemy
source .virtualenvs/dbproj/bin/activate
pip3 install sqlalchemy
pip3 install psycopg2
deactivate
python3
source .virtualenvs/dbproj/bin/activate
python3
psql --version
dir
deactivate
cd ~
wget http://www.cs.columbia.edu/~biliris/4111/21f/projects/proj1-3/webserver.tar
tar xf webserver.tar
mv webserver project
cd project/
git config --global user.name "Man Huang Ho"
git config --global user.email "manhuang1996@gmail.com
exit

git config --global user.email "manhuang1996@gmail.com"
git init
git remote add origin https://github.com/manhuang68/w4111-proj1.git
git add --all
git commit -m "initial commit"
git push -u origin master
dir
vim server.py 
python server.py
cd ..
source .virtualenvs/dbproj/bin/activate
cd project/
python server.py 
vim server.py 
python server.py 
exit
cd project/
vim server.py 
source .virtualenvs/dbproj/bin/activate
cd ..
source .virtualenvs/dbproj/bin/activate
cd project/
python server.py
cd project/cd ..
vim test.py
python server.py --help
python server.py --debug
python server.py --help
python server.py
python test.py
python server.py
cd project/
python server.py
source .virtualenvs/dbproj/bin/activate
cd ..
source .virtualenvs/dbproj/bin/activate
cd project/
python server.py
cd ..
mkdir test
cd test
vim quotes.py
mkdir templates
vim index.html
cd ..
dir
cd test/
dir
python quotes.py
vim index.html
vim quotes.py
python quotes.py
cd ..
pip3 install flask-sqlalchemy
cd test/
python quotes.py
pip3 install flask-sqlalchemy
vim quotes.py
python quotes.py
vim quotes.py
python quotes.py
vim quotes.py
python quotes.py
vim quotes.py
python quotes.py
dir
cd templates/
dir
vim index.html
python quotes.py
cd ..
python quotes.py
cd templates/
vim index.html
cd ..
python quotes.py
psql

psql -U mh4142 -h 35.196.73.133 -d proj1part2
