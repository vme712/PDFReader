FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8

WORKDIR /home/daemon/backend

RUN mkdir -p /var/run/celery-beat \
    && chown daemon /var/run/celery-beat

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends ca-certificates wget \
    aria2 \
    # DELETE NEXT LINE IF YOU READ THIS
    vim-tiny \
    # apt-fast speeds up the image build
    && wget --no-verbose -O /root/apt-fast.tar.gz \
       https://github.com/ilikenwf/apt-fast/archive/3a6bd771bdbbacb21527d593f9fb54909dc1a56f.tar.gz \
    && tar -C /root -xzf /root/apt-fast.tar.gz \
    && mv /root/apt-fast*/apt-fast /usr/bin/ \
    && mv /root/apt-fast*/apt-fast.conf /etc/ \
    && echo 'APT::Default-Release "bullseye";' > /etc/apt/apt.conf.d/99defaultrelease

ENV VIRTUAL_ENV /home/daemon/venv

RUN apt-get update -y \
    && apt-fast install -y --no-install-recommends -t bullseye \
    gcc python3.9 python3-dev musl-dev \
    python3-pip python3-setuptools python3-virtualenv virtualenv \
    # \/ directly from /requirements/base.txt
    python3-bcrypt python3-pil python3-psycopg2 python3-regex \
    # \/ django-storage-swift
    python3-netifaces \
    # \/ geospatial + geoip
    python3-gdal libgeos-3.9.0 libmaxminddb0 \
    # \/ collectstatic
    libmagic1 \
    # \/ makemessages/compilemessages
    gettext \
    python3-twisted python3-msgpack python3-hiredis \
    && apt-get clean -y \
    # \/ We need venv in order to not mess up with python 3.5 which debian installs anyway
    && virtualenv --system-site-packages -p `which python3.9` "$VIRTUAL_ENV"

ENV PATH="$VIRTUAL_ENV/bin:${PATH}"

COPY ./requirements.txt /requirements/

RUN pip install --no-input -r /requirements/requirements.txt

RUN apt-get autoremove -y gcc

COPY . /home/daemon/backend

RUN chmod 777 manage.py

