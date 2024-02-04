FROM python:3.10-bullseye
EXPOSE 80

ARG USERNAME=adeyomola

RUN adduser $USERNAME && apt update -y && apt install apache2 apache2-dev sudo -y && pip install mod_wsgi==5.0.0
RUN echo "$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/apache2, /usr/local/bin/mod_wsgi-express" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN mkdir -p /verba/verba

COPY verba /verba/verba
COPY ./scripts/conf_editor.sh /home/$USERNAME/.local/bin
COPY ./wsgi.py /verba

RUN chmod +x /home/$USERNAME/.local/bin/conf_editor.sh

USER $USERNAME
WORKDIR /verba
RUN pip install -r verba/requirements.txt
ENTRYPOINT ["/bin/bash", "-c", "export PATH=$PATH:/home/adeyomola/.local/bin \
    && conf_editor.sh \
    && flask db-init \
    && sudo mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null"]