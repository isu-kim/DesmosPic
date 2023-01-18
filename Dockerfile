##########################################################
# DesmosPics as Docker container                         #
# Dockerfile by Isu Kim @ https://github.com/isu-kim     #
##########################################################

FROM ubuntu
MAINTAINER isukim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get install -y apache2 git build-essential curl software-properties-common libagg-dev libpotrace-dev pkg-config php php-curl libgl1-mesa-glx
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.7 python3-pip python3.7-distutils
COPY frontend/ /var/www/html/
COPY backend.py /DesmosPics/backend.py
COPY requirements.txt /DesmosPics/requirements.txt
RUN rm /var/www/html/index.html
RUN python3.7 -m pip install --upgrade pip setuptools wheel
RUN python3.7 -m pip install -r /DesmosPics/requirements.txt
EXPOSE 80
EXPOSE 5001
ENTRYPOINT service apache2 restart && python3.7 /DesmosPics/backend.py


