#!/bin/bash
set -o errexit

gunicorn SonorAI.wsgi:application --bind 0.0.0.0:$PORT