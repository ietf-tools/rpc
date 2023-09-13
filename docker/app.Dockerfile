FROM python:3
RUN apt-get -q update && apt-get -qy install netcat-openbsd
ADD https://raw.githubusercontent.com/eficode/wait-for/v2.2.4/wait-for /usr/local/bin/
RUN chmod +rx /usr/local/bin/wait-for
WORKDIR /workspace
COPY requirements.txt /workspace/
RUN pip install -r requirements.txt
COPY . /workspace
COPY docker/app-init.sh /docker-init.sh
