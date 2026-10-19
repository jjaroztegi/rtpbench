FROM python:3.14-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170
RUN apt-get update \
    && apt-get install -y --no-install-recommends iproute2 iptables tcpdump \
    && rm -rf /var/lib/apt/lists/*
# TLS records and SRTP need AES, which the standard library lacks; pinned as uv.lock pins them
RUN pip install --no-cache-dir cryptography==50.0.2 cffi==2.1.1 pycparser==3.11
COPY src /app/src
COPY corpus /app/corpus
ENV PYTHONPATH=/app/src PYTHONUNBUFFERED=1
