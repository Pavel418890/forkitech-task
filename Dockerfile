FROM python:3.11-slim-buster AS builder

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir=/wheels -r /requirements.txt


FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST redis

ARG BACKEND_PORT
ENV DEBUG true
ENV BACKEND_PORT ${BACKEND_PORT}

# copy from first layer pip wheels dependencies
COPY --from=builder /wheels /wheels

# install dependencies
RUN apt update && \
    pip install -U setuptools pip wheel && \
    pip install --no-cache-dir --no-deps /wheels/*
RUN echo ${BACKEND_PORT}

COPY *.py .

LABEL org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.title="forkitech-task" \
    org.opencontainers.image.authors="Pavel Lots <plots418890@gmail.com>" \
    org.opencontainers.image.source="https://github.com/pavel418890/forkitech-task" \
    org.opencontainers.image.revision="${VCS_REF}" \
    org.opencontainers.image.vendor="Pavel Lots"

CMD uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT
