#!/bin/bash

PROJECT="/opt/swiper"

cat $PROJECT/backend/logs/gunicorn.pid | xargs kill -HUP
