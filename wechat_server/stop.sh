curl http://127.0.0.1:8081/bot_logout_all
sleep 3

uwsgi --stop uwsgi8081.pid
#uwsgi --stop uwsgi8082.pid
