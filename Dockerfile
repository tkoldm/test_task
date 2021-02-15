FROM python:3.8.1-slim-buster
RUN adduser task
WORKDIR /home/application

COPY requirements.txt requirements.txt
RUN python -m venv task
RUN task/bin/pip install -r requirements.txt
RUN task/bin/pip install gunicorn

COPY . .
ENV FLASK_APP=task.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN chmod +x boot.sh
USER task
EXPOSE 5000

ENTRYPOINT ["sh", "./boot.sh" ]