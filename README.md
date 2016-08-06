# HIMS SERVER (v2.5)

    This project is HIMS Server that is based on Flask Web Framework 
    Whole server-side codes are archived in here. It's simple but doing a lot of functions.
    Because of code management efficiency, this hims-server is a single project.
    It covers both of hims-host(for employee) and hims-guest(for guest).
    HIMS is B2B service that provide intelligent management system for HOTEL.
    Since Number of user is not that big, HIMS does not need to be scalable. 

## Table of Content

* <a id="content1" href="#body1">1. Summary</a>
* <a id="content2" href="#body2">2. Application Architecture</a>
* <a id="content3" href="#body3">3. Server Architecture</a>
* <a id="content4" href="#body4">4. Requirement</a>
* <a id="content5" href="#body5">5. Configuration</a>
* <a id="content6" href="#body6">6. Installation</a>
* <a id="content7" href="#body7">7. Testing</a>
* <a id="content8" href="3body8">8. Deploy</a>

## <a id="body1" href="#content1">1. Summary</a>
## <a id="body2" href="#content2">2. Application Architecture</a>


![image](https://cloud.githubusercontent.com/assets/8446067/14774196/64231712-0aee-11e6-86d2-94145c76aaed.png)

![hims_server](https://cloud.githubusercontent.com/assets/8446067/14774220/94f44258-0aee-11e6-9d68-090f1ab71b0b.png)

## <a id="body3" href="#content3">3. Server Architecture</a>
## <a id="body4" href="#content4">4. Requirement</a>

* OS : Ubuntu 14.04
* Python Version : Python 2.7.11

## <a id="body5" href="#content5">5. Configuration</a>
## <a id="body6" href="#content6">6. Installation</a>

Run following commands

```shell
sudo apt-get update
sudo apt-get -y --force-yes install python-pip libpq-dev python-dev libssl-dev git libffi-dev nginx npm nodejs-legacy libjpeg-dev libjpeg8-dev
sudo pip install virtualenv
sudo adduser ubuntu www-data
sudo mkdir /var/www
sudo chown -R ubuntu:www-data /var/www
sudo chmod -R g+rwX /var/www
mkdir /var/www/dodotdo
mkdir /var/www/dodotdo/hims-server
cd /var/www/dodotdo/hims-server
git init
git remote add origin https://<github_userid>:<github_password>@github.com/dodotdo/hims-server.git
git pull origin develop-kr-dev
cd app_server
virtualenv venv
source venv/bin/activate

pip install --no-cache-dir -I pillow
pip install -r requirements.txt

./starthims.sh
python manager.py initall
./starthims.sh

sudo ln -f hims_nginx.conf /etc/nginx/conf.d/hims_nginx.conf
sudo rm /etc/nginx/sites-enabled/default

mkdir /var/www/dodotdo/hims_guest_web
cd /var/www/dodotdo/hims_guest_web
git init
git remote add origin https://<github_userid>:<github_password>@github.com/dodotdo/hims-guest-web.git
git pull origin develop
sudo npm install -g bower
bower install
sudo npm install
sudo npm install -g gulp-cli
HOTEL_INFO=<hotel name> NODE_ENV=production gulp build

mkdir /var/www/dodotdo/hims_host_web
cd /var/www/dodotdo/hims_host_web
git init
git remote add origin https://<github_userid>:<github_password>@github.com/dodotdo/hims-host-web.git
git pull origin develop
sudo npm install -g bower
bower install
sudo npm install
sudo npm install -g gulp-cli
HOTEL_INFO=<hotel name> NODE_ENV=production gulp build

cp -r /var/www/dodotdo/hims_guest_web/build/assets/* /var/www/dodotdo/hims_host_web/build/assets/

sudo /etc/init.d/nginx start
```


## <a id="body7" href="#content7">7. Testing</a>
## <a id="body8" href="#content8">8. Deploy</a>


* ```sudo apt-get install nginx```
* ```sudo ln -f hims_nginx.conf /etc/nginx/conf.d/```
* TODO : **Docker** deployment shipping system


## <a id="body9" href="#content9">9. Dependency</a>

### Dependancy

| Dependancy | Version | Description |
| --- | --- | --- |
|alembic|0.8.2||
|amqp|1.4.9||
|aniso8601|1.1.0||
|anyjson|0.3.3||
|bcrypt|2.0.0||
|beautifulsoup4|4.4.1||
|billiard|3.3.0.23||
|blinker|1.4||
|boto|2.38.0||
|celery|3.1.23||
|cffi|1.4.2||
|connexion|1.0.67||
|coverage|4.0.3||
|decorator|4.0.2||
|eventlet|0.18.4||
|flasgger|0.5.12||
|Flask|0.10.1||
|Flask-Assets|0.11||
|Flask-Bcrypt|0.6.2||
|Flask-Cache|0.13.1||
|Flask-Celery|2.4.3||
|Flask-Cors|2.1.2||
|flask-csrf|0.9.2||
|Flask-HTTPAuth|2.6.0||
|flask-log|0.1.0||
|Flask-Logging|0.1.3||
|Flask-Login|0.3.2||
|Flask-Mail|0.9.1||
|Flask-Migrate|1.6.0||
|Flask-Principal|0.4.0||
|Flask-Redis|0.1.0||
|Flask-RESTful|0.3.5||
|flask-restful-swagger|0.19||
|Flask-S3|0.1.7||
|Flask-Script|0.6.3||
|Flask-Security|1.7.4||
|Flask-Sessions|0.1.5||
|Flask-SocketIO|2.2||
|Flask-SQLAlchemy|1.0||
|flask-swagger|0.2.12||
|Flask-Uploads|0.1.3||
|funcsigs|0.4||
|functools32|3.2.3.post2||
|gcm|0.3||
|google-api-python-client|1.5.0||
|greenlet|0.4.9||
|gunicorn|19.4.5||
|httpauth|0.2||
|httplib2|0.9.2||
|itsdangerous|0.24||
|Jinja2|2.8||
|jsonschema|2.5.1||
|kombu|3.0.35||
|logging|0.4.9.6||
|Mako|1.0.3||
|MarkupSafe|0.23||
|migrate|0.3.7||
|mistune|0.7.2||
|mock|1.3.0||
|modulegraph|0.10.4||
|Naked|0.1.31||
|oauth2client|2.0.1||
|passlib|1.6.5||
|pathlib|1.0.1||
|pbr|1.8.1||
|Pillow|2.9.0||
|psycopg2|2.6.1|PATH에 PostgreSQL이 등록되어 있어야 한다. .bash_profile에 `export PATH="/Applications/Postgres.app/Contents/Versions/9.5/bin:$PATH"` 추가|
|pyasn1|0.1.9||
|pyasn1-modules|0.0.8||
|pycparser|2.14||
|pycrypto|2.6.1||
|PyJWT|1.4.0||
|pyparsing|2.0.1||
|python-bcrypt|0.3.1||
|python-dateutil|2.4.2||
|python-editor|0.5||
|python-engineio|0.8.6||
|python-json-logger|0.1.4||
|python-logstash|0.4.5||
|python-openid|2.2.5||
|python-socketio|1.1||
|pytz|2016.3||
|PyYAML|3.11||
|redis|2.10.5||
|requests|2.9.1||
|rsa|3.4.2||
|shellescape|3.4.1||
|simplejson|3.8.2||
|six|1.10.0||
|SQLAlchemy|1.0.12||
|strict-rfc3339|0.6||
|uritemplate|0.6||
|webassets|0.11.1||
|Werkzeug|0.11.2||
|WTForms|1.0.5||
