docker run -it -p 8020:8020 \
     -e DJANGO_SUPERUSER_USERNAME=root \
     -e DJANGO_SUPERUSER_PASSWORD=mypassword \
     -e DJANGO_SUPERUSER_EMAIL=root@example.com \
     shorturl-v01.
