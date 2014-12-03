SakilaOkk
==========

This repository contains a Django project to render the MySQL Database Sakila in a Web Application.

## Prerequisites:
This application requires Django 1.6.5, if you don't have it you can get it by:

```
    # Installing pip (Python Package Index)
    $ sudo easy_install pip

    # Installing Django 1.6.5
    $ sudo pip install django==1.6.5

    # Installing MySQL for Python
    $ sudo pip install MySQL-python
```

**NOTE: If you get an error "No Module Name Called MySQLdb" do the following:**

```
    $ brew install mysql
    $ sudo pip install MySQL-python

```

## Installation & Running the Application

```
    # Navigate to a directory to save the app
    $ cd /path/to/save/app

    # Download the app
    $ git clone https://github.com/alkhenji/SakilaOkk.git

    # Switch to that directory
    $ cd SakilaOkk

    # Run the application (localhost:8000)
    $ python manage.py runserver
```

To run the application on a different port: `$ python manage.py runserver 8008` where 8008 is the port number that you want.

## Connecting the Database:
You will need to be connected to the CMUQ-SECURE network to be able to access the database. If you are using it from outside CMUQ, you will need to use a VPN to gain access to the database.

... and that's it :)!

**Note: To populate the database with the scripts, use the mssql.sql file. The commented out procedures are done with Django**

## Developers:
Omar Ragheeb (O), Abdulla AlKhenji (K), Khaled Fares (K)
