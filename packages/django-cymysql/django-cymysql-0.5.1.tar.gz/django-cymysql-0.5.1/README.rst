django-cymysql
==============

Django mysql database backend for cymysql

Requirements
-------------

* Django 1.10, 1.11
* CyMySQL (https://github.com/nakagami/CyMySQL) 0.8.9+

Installation
------------

::

    $ pip install cymysql
    $ pip install django-cymysql

Database
------------

* Create database (set default character set to 'utf8')

::

    mysql> create database some_what_database default character set utf8;

Settings
------------

::

    DATABASES = {
        'default': {
            'ENGINE': 'mysql_cymysql',
            'NAME': 'some_what_database',
            'HOST': ...,
            'USER': ...,
            'PASSWORD': ...,
        }
    }
