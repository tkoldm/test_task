#!/bin/bash
celery -A app.celery worker -B -l info 