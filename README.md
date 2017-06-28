# Django-Imager [![Build Status](https://travis-ci.org/carloscadena/django-imager.svg?branch=master)](https://travis-ci.org/carloscadena/django-imager) [![Coverage Status](https://coveralls.io/repos/github/carloscadena/django-imager/badge.svg?branch=master)](https://coveralls.io/github/carloscadena/django-imager?branch=master)

Simple image management website using Django

## Authors
- Ely Paysinger
- Carlos Cadena

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

## Routes
- /
- /login
- /logout
- /account/register
- /profile
- /admin

## Models
### User
- username
- email
- password
### Profile
- user
- location
- creation date
- birthday
- photog_level
- website
- headline
- active
### Photo
- title
- description
- profile
- image
- date_uploaded
- date_modified
- date_published
- published =
### Album
- profile
- title
- date_uploaded
- date_modified
- date_published
- published
- cover_photo
- photos
