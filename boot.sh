#!/bin/bash
flask --help
flask db init
flask db --help
flask db migrate
flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - task:app