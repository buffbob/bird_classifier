FROM python:latest

RUN adduser classifier

WORKDIR /home/classifier

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY classifier classifier
COPY config.json hell.py init_db.py run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R classifier:classifier ./
USER classifier


EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
