FROM debian:buster-slim

RUN apt-get update && \
    apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    libmariadbclient-dev \
    libapache2-mod-wsgi-py3 \
    openssh-client \
    gcc \
    python3-dev \
    glade \
    nano --no-install-recommends 

COPY . /app/
WORKDIR /app/

COPY ./videojuego.conf /etc/apache2/sites-available/videojuego.conf

RUN a2ensite videojuego.conf

# COPY ./videojuegosD /app/videojuegosD

RUN chown :www-data /app/media/
RUN chmod 775 /app/media/

RUN pip3 install --upgrade setuptools


RUN pip3 install --no-cache-dir -r /app/requeriments.txt

EXPOSE 8080
# RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

RUN apt-get clean 

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# CMD ["apachectl", "-D", "FOREGROUND"]