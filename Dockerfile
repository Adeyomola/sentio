FROM python:3.10-bullseye
EXPOSE 80

ARG USERNAME=adeyomola

RUN adduser adeyomola && apt update -y \
    && apt install apache2 apache2-dev --prefix=/home/$USERNAME/.local/bin -y
RUN mkdir -p /verba/verba

COPY verba /verba/verba
COPY ./wsgi.py /verba
COPY ./scripts/conf_editor.sh /home/$USERNAME/.local/bin

RUN chmod +x /home/$USERNAME/.local/bin/conf_editor.sh

USER $USERNAME
WORKDIR /verba
RUN pip install -r verba/requirements.txt
ENTRYPOINT ["/bin/bash", "-c", "export PATH=$PATH:/home/adeyomola/.local/bin \
    && conf_editor.sh \
    && flask db-init \
    && mod_wsgi-express start-server wsgi.py --user adeyomola --group adeyomola --port 80 --processes 2 --envvars .env \
    && tail -f /dev/null"]