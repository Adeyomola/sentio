FROM python:3.10-bullseye
EXPOSE 80

RUN mkdir -p /sentio/sentio

COPY sentio /sentio/sentio
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /sentio

RUN ["/bin/bash", "-c", "adduser adeyomola && apt update -y && apt install apache2 apache2-dev -y"]

WORKDIR /sentio/sentio
RUN ["/bin/bash", "-c", "pip install -r requirements.txt"]

WORKDIR /sentio
ENTRYPOINT ["/bin/bash", "-c", "conf_editor.sh && flask db-init && mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --envvars .env && tail -f /dev/null"]
