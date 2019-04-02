#!/bin/bash

PROJECT="/opt/swiper"

# 关掉 gunicorn
cat $PROJECT/backend/logs/gunicorn.pid | xargs kill
