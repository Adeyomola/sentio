FROM python:3.10-bullseye
EXPOSE 80

RUN mkdir -p /verba/verba

COPY verba /verba/verba
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /verba

ARG USERNAME=adeyomola

RUN ["/bin/bash", "-c", "adduser $USERNAME && apt update -y && apt install apache2 apache2-dev sudo -y \
    && echo 'adeyomola ALL=(ALL) NOPASSWD: /bin/chmod, /usr/local/bin/conf_editor.sh, /usr/local/bin/flask, /usr/local/bin/mod_wsgi-express' > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME"]

USER $USERNAME
WORKDIR /verba/verba
RUN ["/bin/bash", "-c", "pip install -r requirements.txt && sudo chmod +x /usr/local/bin/conf_editor.sh"]

WORKDIR /verba
ENTRYPOINT ["/bin/bash", "-c", "sudo conf_editor.sh && sudo flask db-init \
    && sudo mod_wsgi-express start-server wsgi.py --user $USERNAME --group $USERNAME --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null"]
