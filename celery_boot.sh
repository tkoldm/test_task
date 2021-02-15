#!/bin/sh
source task/bin/activate
celery -A app.celery worker -B -l info 