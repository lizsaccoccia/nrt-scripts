


#### THIS IS A PLACEHOLDER TO DEVELOP THE PYDAP CONNECTOR AROUND ####



FROM python:2.7
MAINTAINER Raul <raul.requero@vizzuality.com>
ARG NAME=python-script
ENV NAME ${NAME}

RUN apt-get install -y \
  gdal-bin \
  libgdal-dev \
  libnetcdf-dev \
  netcdf-bin \
  cron \
  && apt-get clean

USER root

RUN groupadd -r $NAME && useradd -r -g $NAME $NAME


RUN mkdir -p /opt/$NAME
COPY requirements.txt /opt/$NAME/requirements.txt
RUN cd /opt/$NAME && pip install -r requirements.txt

COPY main.py /opt/$NAME/main.py

# Copy the application folder inside the container
WORKDIR /opt/$NAME

COPY ./src /opt/$NAME/src
COPY ./data /opt/$NAME/data

RUN chown $NAME:$NAME /opt/$NAME
USER $NAME

VOLUME /opt/$NAME/data

# Launch script
CMD ["python", "main.py"]
