FROM python:3.10-bullseye
EXPOSE 80

ARG USERNAME=adeyomola

RUN mkdir -p /verba/verba && adduser $USERNAME && apt update -y && apt install apache2 apache2-dev -y

COPY verba /verba/verba
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /verba

WORKDIR /verba/verba
RUN pip install -r requirements.txt && chmod +x /usr/local/bin/conf_editor.sh

WORKDIR /verba
ENTRYPOINT conf_editor.sh && flask db-init \
    && mod_wsgi-express start-server wsgi.py --user $USERNAME --group $USERNAME --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null