
OS=""
case "$OSTYPE" in
  solaris*) OS="SOLARIS" ;;
  darwin*)  OS="OSX" ;;
  linux*)   OS="LINUX" ;;
  bsd*)     OS="BSD" ;;
  *)        OS="unknown: $OSTYPE" ;;
esac

echo -n "Github userid > "
read github_userid
echo -n "Github password > "
read -s github_password
echo 
echo -n "Hotel Name > "
read hotel_name
echo -n "REDIRECT URL ex) http://hotelnhims.com > "
read server_url
echo -n "sudo password > "
read -s password
echo

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
brew install git python3 nginx npm uwsgi
if [ ! -e "/usr/local/var/www/" ]; then 
    mkdir /usr/local/var/www
fi
cd /usr/local/var/www/
mkdir hims-server hims-guest-web hims-host-web hims-entry
echo $password | sudo -S chgrp _www hims-server hims-guest-web hims-host-web hims-entry

cd hims-server
git init
git remote add origin https://$github_userid:$github_password@github.com/dodotdo/hims-server.git
git pull origin develop-python3.5
git checkout develop-python3.5
cd app_server
virtualenv -p python3 venv
source venv/bin/activate
pip install pip --upgrade
pip install -r requirements.txt --upgrade

cd ..

sudo mkdir /var/log/nginx
sudo mkdir /var/log/uwsgi
sudo chgrp _www /var/log/nginx
sudo chgrp _www /var/log/uwsgi

if [ "$OS" == "OSX" ]; then
    echo 'nginx restart'
    sudo ln -f nginx.conf /usr/local/etc/nginx/nginx.conf
    sudo nginx -s stop
    sudo nginx
else
    sudo ln -f nginx.conf /etc/nginx/nginx.conf
    /etc/init.d nginx restart
fi
./stophims.sh
./starthims.sh
deactivate

cd ../hims-guest-web
git init
git remote add origin https://$github_userid:$github_password@github.com/dodotdo/hims-guest-web.git
git pull origin develop
git checkout develop
sudo npm install -g bower
bower install
npm install --production
sudo npm install -g gulp-cli
HOTEL_INFO=$hotel_name NODE_ENV=production SOCKET_SSL=false SOCKET_SECURE=false REDIRECT_URL=$server_url gulp build

cd ../hims-host-web
git init
git remote add origin https://$github_userid:$github_password@github.com/dodotdo/hims-host-web.git
git pull origin develop
git checkout develop
bower install
npm install --production
HOTEL_INFO=$hotel_name NODE_ENV=production SOCKET_SSL=false SOCKET_SECURE=false  REDIRECT_URL=$server_url gulp build

cp -r ../hims-guest-web/build/assets/* build/assets/

cd ../hims-entry
deacitvate
git init
git remote add origin https://$github_userid:$github_password@github.com/dodotdo/hims-entry.git
git pull origin develop-python3.5
git checkout develop-python3.5
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manager.py createdb

sudo kill -9 $(ps aux | grep uwsgi | awk '{print $2}')
screen -X -S entry quit
screen -S entry -d -m sudo uwsgi --ini hims_uwsgi.ini
deactivate
cd ../hims-server
cd app_server
source venv/bin/activate
python manager.py initall
