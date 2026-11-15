FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928
RUN apt-get update \
    && apt-get install -y --no-install-recommends iproute2 iptables tcpdump \
    && rm -rf /var/lib/apt/lists/*
# TLS records and SRTP need AES, which the standard library lacks; pinned as uv.lock pins them
RUN pip install --no-cache-dir cryptography==50.0.2 cffi==2.1.1 pycparser==3.11
# the package in the build context: a checkout's src/rtpbench, or an installed rtpbench's own
# directory (.), which holds this file and the corpus too
ARG RTPBENCH_SRC=src/rtpbench
COPY ${RTPBENCH_SRC}/*.py /app/src/rtpbench/
COPY corpus /app/corpus
ENV PYTHONPATH=/app/src PYTHONUNBUFFERED=1
