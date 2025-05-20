FROM python:3.9-alpine3.13
LABEL maintainer="Andre"

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/py
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ARG DEV=false
RUN python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip && \
    apk add --update --no-cache \
        postgresql-client jpeg-dev zlib zlib-dev \
        libffi-dev openssl-dev libc6-compat && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
USER django-user
