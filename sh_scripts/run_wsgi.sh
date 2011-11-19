sudo uwsgi -p 4 --pythonpath=/home/ubuntu/webapps/stud2dotoh --module wsgi --socket /tmp/uwsgi.sock -d /var/log/stud2dotoh/uwsgi.log

