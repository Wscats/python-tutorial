#!/bin/bash

PROJECT="/opt/swiper"

cd $PROJECT/backend
source $PROJECT/.venv/bin/activate
gunicorn -c swiper/gunicorn-config.py swiper.wsgi
deactivate
cd -
