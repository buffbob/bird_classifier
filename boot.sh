#!/bin/bash
source venv/bin/activate
exec python3 run.py
#see below for non-local install
#exec gunicorn -b :5000 --access-logfile - --error-logfile - classifier:app
