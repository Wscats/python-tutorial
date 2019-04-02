#!/bin/bash

celery worker -A worker --loglevel=info
