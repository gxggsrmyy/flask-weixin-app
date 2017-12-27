FROM ubuntu:16.04

RUN \
  export TZ="Asia/Shanghai" && \
  sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
  sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
  apt-get update -y && \
  apt-get upgrade -y && \
  apt-get install \
    build-essential \
    curl \
    libffi-dev \
    libssl-dev \
    python-dev \
    python-pip -y \
    uuid-runtime \
    vim \
    tzdata \
    && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
  curl https://phuslu.github.io/bashrc >/root/.bashrc

COPY requirements.txt /opt/weixin/

RUN pip install --proxy http://cn.phus.lu:8080 -r /opt/weixin/requirements.txt

ADD . /opt/weixin/

CMD ["/usr/bin/python", "/opt/weixin/wxmain.py"]
