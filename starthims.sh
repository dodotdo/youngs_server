#!/bin/bash

OS=""
case "$OSTYPE" in
  solaris*) OS="SOLARIS" ;;
  darwin*)  OS="OSX" ;;
  linux*)   OS="LINUX" ;;
  bsd*)     OS="BSD" ;;
  *)        OS="unknown: $OSTYPE" ;;
esac
echo $OS
cd app_server
source venv/bin/activate
cd ..
if screen -list | grep -q "redis"; then
    echo 'redis process running'
else
    redis_server_script="./app_server/redis-3.2.0/src/redis-server"
    if [ -e $redis_server_script ]; then
        echo "redis by var exists"
    else
        cd app_server
        if ! -e "./redis-3.2.0.tar.gz"; then
            if [ "$OS" == "OSX" ]; then
                curl -o "redis-3.2.0.tar.gz" "http://download.redis.io/releases/redis-3.2.0.tar.gz"
            else
                wget "http://download.redis.io/releases/redis-3.2.0.tar.gz"
            fi
            tar -xvzf redis-3.2.0.tar.gz
        fi
        cd redis-3.2.0
        make
        cd ../../
    fi
    echo 'run redis'
    screen -S redis -d -m app_server/redis-3.2.0/src/redis-server redis.conf
fi

if screen -list | grep -q "celery"; then
    echo 'celery process running'
else
    cd app_server
    screen -S celery -d -m celery worker -A youngs_server.youngs_app.celery -P eventlet --loglevel=debug
    cd ..
    echo 'run celery'
fi

if screen -list | grep -q "beat"; then
    echo 'celery beat running'
else
    cd app_server
    screen -S beat -d -m celery -A youngs_server.youngs_app.celery beat -l info
    cd ..
    echo 'run beat'
fi

if screen -list | grep -q "gunicorn"; then
    echo 'gunicorn process running'
else
    cd app_server
    screen -S gunicorn -d -m gunicorn -b 0.0.0.0:8080 --worker-class eventlet -w 1 run:app
    cd ..
    echo 'run gunicorn'
fi

if screen -list | grep -q "tcp"; then
    echo 'tcp socket running'
else
    cd socket_server
    screen -S tcp -d -m python run.py
    echo 'run tcp'
    cd ..
fi 

