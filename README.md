# Django-Imager [![Build Status](https://travis-ci.org/carloscadena/django-imager.svg?branch=master)](https://travis-ci.org/carloscadena/django-imager)

Simple image management website using Django

##Authors
-Ely Paysinger
-Carlos Cadena

## To Install:
Clone this repository
```
git clone https://github.com/carloscadena/django-imager.git
```
Start up a new virtual environment.
```
$ cd django-imager
$ python3 -m venv ENV
$ source ENV/bin/activate
```
Once your environment has been activated, install Django and required packages.
```
(ENV) $ pip install -r requirements.pip
```
Navigate to the project root, imagersite, and apply the migrations for the app.
```
(ENV) $ cd imagersite

(ENV) $ ./manage.py migrate
```
Run the server in order to server the app on localhost
```
(ENV) $ ./manage.py runserver
```
[Django serves on port 8000](http://localhost:8000)
