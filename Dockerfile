FROM python:3.10-bullseye
EXPOSE 80

ARG USERNAME=adeyomola

RUN adduser $USERNAME && apt update -y && apt install apache2 apache2-dev sudo -y \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL " > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME && mkdir -p /verba/verba

COPY verba /verba/verba
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /verba

WORKDIR /verba/verba
RUN chmod +x /usr/local/bin/conf_editor.sh && pip install -r requirements.txt

USER $USERNAME
WORKDIR /verba
ENTRYPOINT sudo conf_editor.sh \
    && sudo flask db-init \
    && sudo mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null