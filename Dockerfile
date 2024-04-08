FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

## Install packages
ENV RUN_LANG_UBUNTU="18.04"
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get update && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

## Install python and its packages install
RUN apt-get install -y python3.7 python3-pip
RUN pip3 install numpy==1.19.4
RUN pip3 install pendulum==2.1.2
RUN pip3 install requests==2.25.0
RUN pip3 install psutil==5.7.3
RUN pip3 install -U pytest
RUN pip3 install pytest-json-report --upgrade
# Post-install
RUN echo 0


## Install NodeJS and its packages
RUN curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
RUN apt-get install -y nodejs
RUN npm install -g jest
RUN npm install -g jest-json-repoter
COPY registry/javascript/packages /packages
COPY registry/javascript/template /template

# Post-install
RUN echo 0

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

COPY run_lang /run_lang
COPY manage.py /
COPY start_run_lang.sh /start_run_lang.sh

WORKDIR /

ENTRYPOINT ["./start_run_lang.sh"]

