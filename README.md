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
- /profile/<user>
- /admin
- /images/albums
- /images/albums/<id>
- /images/albums/add
- /images/photos/
- /images/photos/add
- /library

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

# Ansible [repo](https://github.com/W-Ely/ansible)

## Requirements
- EC2, RDS, and S3 setup.  <--- more complicated than I can layout here
- EC2, RDS resource
-- [Irreverently Me - From 0 to 60 with Django on AWS](https://irreverently.me/2015/07/05/from-0-to-60-with-django-on-aws/)
- S3 resources
-- [Dan Poirier - Using Amazon S3 to Store your Django Site's Static and Media Files](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/)
-- [Jorge Chang - HOWTO: Deploy a fault tolerant Django app on AWS – Part 2: Moving static and media files to S3](http://www.jorgechang.com/blog/howto-deploy-a-fault-tolerant-django-app-on-aws-part-2-moving-static-media-files-to-s3/)


## Usage
- clone ansible repo: ```git clone https://github.com/W-Ely/ansible.git```
- cd into dir: ```cd ansible```
- create a "hosts" file with your variables inside following the format in hosts_template
- run ansible playbook to deploy: ```ansible-playbook -i hosts playbooks/django-project.yml```
