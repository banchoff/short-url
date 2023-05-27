FROM python:3.10-buster

# Install nginx
RUN apt-get update && apt-get install nginx vim sqlite3 -y --no-install-recommends
COPY nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# Copy source and install dependencies
RUN mkdir -p /opt/app/shorturl
RUN mkdir -p /opt/app/pip_cache
COPY requirements.txt start-server.sh /opt/app/
RUN chmod +x /opt/app/start-server.sh
COPY shorturl /opt/app/shorturl/
WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN rm /opt/app/shorturl/db.sqlite3
RUN python3 /opt/app/shorturl/manage.py makemigrations
RUN python3 /opt/app/shorturl/manage.py migrate
RUN chown -R www-data:www-data /opt/app

# Just in case there are temporary files...
RUN find /opt/app/shorturl -name "*~" -exec /bin/rm {} \;
RUN find /opt/app/shorturl -name "*.swp" -exec /bin/rm {} \;

# Start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
