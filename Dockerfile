FROM python:3.10-bullseye
EXPOSE 80

ARG USERNAME=adeyomola

RUN mkdir -p /verba/verba

COPY verba /verba/verba
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /verba

WORKDIR /verba/verba
RUN adduser $USERNAME && apt update -y && apt install apache2 apache2-dev sudo -y && pip install -r verba/requirements.txt \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/apache2, /usr/local/bin/mod_wsgi-express, /usr/local/bin/conf_editor.sh, /usr/local/bin/flask" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME && chmod +x /usr/local/bin/conf_editor.sh

USER $USERNAME
WORKDIR /verba
ENTRYPOINT ["/bin/bash", "-c", "sudo conf_editor.sh \
    && sudo flask db-init \
    && sudo mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null"]