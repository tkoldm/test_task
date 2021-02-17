FROM python:3.8.1-slim-buster

RUN adduser task

WORKDIR /home/task

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY task.py config.py boot.sh ./

ENV FLASK_APP=task.py

RUN chmod +x boot.sh
RUN chown -R task:task ./
USER task

EXPOSE 5000
ENTRYPOINT ["sh", "./boot.sh"]