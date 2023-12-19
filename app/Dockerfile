FROM python:3.10-bullseye
RUN mkdir -p /sentio/sentio

COPY sentio /sentio/sentio
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /sentio

RUN ["/bin/bash", "-c", "adduser adeyomola && apt update && apt install apache2 apache2-dev"]

WORKDIR /sentio/sentio
RUN ["/bin/bash", "-c", "pip install -r requirements.txt"]

WORKDIR /sentio
RUN ["/bin/bash", "-c", "conf_editor && sudo ./sentio/.venv/bin/mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --envvars .env"]