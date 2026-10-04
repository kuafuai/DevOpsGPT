FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

## PYTHON

RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update
RUN apt install python3.10 -y
RUN apt install python3.10-dev python3.10-venv python3-pip -y 

# Utils
RUN apt install -y curl \
    lsof \
    git \
    sqlite3

COPY ./ /app

RUN chmod +x /app/run.sh

RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/requirements.txt

WORKDIR /app
EXPOSE 8080 8081

ENTRYPOINT ["/app/run.sh"]
