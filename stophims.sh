sudo kill -9 $(ps aux | grep celery | awk '{print $2}')
sudo kill -9 $(ps aux | grep redis | awk '{print $2}')
sudo kill -9 $(ps aux | grep tcp | awk '{print $2}')
sudo kill -9 $(lsof -t -i:5555)
sudo kill -9 $(sudo lsof -t -i:8080)
sudo kill -9 $(sudo lsof -t -i:6379)
screen -wipe
screen -X -S celery quit 
screen -X -S gunicorn quit
screen -X -S beat quit
screen -X -S tcp quit
screen -X -S redis quit
