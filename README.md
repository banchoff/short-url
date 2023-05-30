# README #

URL Shortener app. Just for fun.

The app is written in Python 3.10.6 and Django 4.2.1. For the DB we use Sqlite3.

It uses ReactJS 18.2 and Bootstrap 5 for the frontend.

Please, see src/requirements.txt

The app itself is in **src/shorturl**. 

### Creating the DB ###

This is required since the app doesn't ship with the DB file.

    cd src/shorturl
    python3 manage.py makemigrations
    python3 manage.py migrate

### Dev run ###

For running the app in dev mode:

    cd src/shorturl
    python3 manage.py runserver

And then access to http://127.0.0.1:8000/ in your web browser.


### Running with Gunicorn ###

For running using Gunicorn:

    cd src/shorturl
    gunicorn shorturl.wsgi

And access to http://127.0.0.1:8000 in your web browser.


### Building the Docker image ###

We can build the image using the Dockerfile provided in this project (see src/Dockerfile).

    cd src
    docker build -t IMAGE_NAME .

### Running the image just created ###

Once we have the image created, for running it just:

    docker run -it -p 8020:8020 \
    	   -e DJANGO_SUPERUSER_USERNAME=root \
	   -e DJANGO_SUPERUSER_PASSWORD=mypassword \
	   -e DJANGO_SUPERUSER_EMAIL=root@example.com \
	   -e DJANGO_DEBUG=False \
	   IMAGE_NAME

Note that when running the app in this mode, all data will be lost when the container is halted. 

### Testing the Docker image ###

You can test the Docker image by running:

	./test_build.sh

This script has a few steps:

* it creates the Docker image, 
* lunches a container based on that image, 
* tests if the given user can or cannot log in,
* and the destroys the container and the image just created.

