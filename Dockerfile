FROM python:3.10-bullseye
EXPOSE 80

RUN mkdir -p /verba/verba

COPY verba /verba/verba
COPY ./scripts/conf_editor.sh /usr/local/bin
COPY ./wsgi.py /verba

ARG USERNAME=adeyomola

RUN ["/bin/bash", "-c", "adduser adeyomola && apt update -y && apt install apache2 apache2-dev sudo -y"]
RUN echo "$USERNAME ALL=(ALL) NOPASSWD: /usr/local/bin/conf_editor.sh" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME && chmod +x /usr/local/bin/conf_editor.sh

USER $USERNAME
WORKDIR /verba
RUN pip install -r verba/requirements.txt
ENTRYPOINT ["/bin/bash", "-c", "export PATH=$PATH:/home/adeyomola/.local/bin \
    && sudo conf_editor.sh \
    && flask db-init \
    && mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null"]