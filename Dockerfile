FROM python:3.8.6-slim-buster

ENV APP_USER=app
ENV APP_DIR=/opt/app

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

RUN useradd -m -s /bin/bash ${APP_USER} \
    && echo "${APP_USER}:${APP_USER}" | chpasswd

WORKDIR ${APP_DIR}
COPY . ./
RUN pip install --no-cache-dir .

USER ${APP_USER}

ENTRYPOINT ["nlp-cli"]
