FROM python:3.10-bullseye
EXPOSE 80

ARG USERNAME=adeyomola

RUN adduser $USERNAME && apt update -y && apt install apache2 apache2-dev sudo -y \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/apache2, /usr/local/bin/conf_editor.sh " > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME && mkdir -p /verba/verba

COPY verba /verba/verba
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /verba

RUN chmod +x /usr/local/bin/conf_editor.sh 

USER $USERNAME
WORKDIR /verba/verba
RUN python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

WORKDIR /verba
ENTRYPOINT ["/bin/bash", "-c", "export PATH=$PATH:/home/adeyomola/.local/bin \
    && sudo conf_editor.sh \
    && flask db-init \
    && sudo mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null"]