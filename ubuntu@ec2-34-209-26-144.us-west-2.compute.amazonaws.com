#!upstart
description "django-imager"

start on runlevel [2345]
stop on runlevel [016]


respawn
setuid nobody
setgid www-data

chdir /home/ubuntu/django-imager/imagersite/imagersite

exec /usr/bin/gunicorn wsgi:application
