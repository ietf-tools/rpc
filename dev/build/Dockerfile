FROM ghcr.io/ietf-tools/rpc-app-base:latest
LABEL maintainer="IETF Tools Team <tools-discuss@ietf.org>"

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd -g 1000 rpc && \
    useradd -c "Purple People Eater" -u 1000 -g rpc -m -s /bin/false purple

COPY . .
COPY ./dev/build/start.sh ./start.sh
COPY ./dev/build/purple-start.sh ./purple-start.sh
COPY ./dev/build/migration-start.sh ./migration-start.sh
COPY ./dev/build/gunicorn.conf.py ./gunicorn.conf.py

RUN pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt

RUN chmod +x start.sh && \
    chmod +x purple-start.sh && \
    chmod +x migration-start.sh

RUN mkdir -p /a

VOLUME [ "/a" ]

EXPOSE 8000

CMD ["./start.sh"]
