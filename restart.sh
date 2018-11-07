uwsgi --stop uwsgi.pid
uwsgi --stop uwsgi8081.pid
uwsgi --stop uwsgi8082.pid

uwsgi --ini uwsgi.ini
uwsgi --ini uwsgi8081.ini
uwsgi --ini uwsgi8082.ini