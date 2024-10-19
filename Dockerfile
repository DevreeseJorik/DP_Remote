FROM stronglytyped/arm-none-eabi-gcc:latest

RUN apt-get update -y &&  \
    apt-get install -y python3.8 python3.8-distutils wget && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3.8 get-pip.py && \
    rm get-pip.py

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && alias python=python3

ADD build /tmp
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

EXPOSE 80
EXPOSE 53/tcp
EXPOSE 53/udp