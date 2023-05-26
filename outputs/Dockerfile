FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install Jinja2

RUN pip3 install PyPDF2

RUN pip3 install click



RUN apt-get update \
    && apt-get install -y --no-install-recommends \

        git \

        ansible \

    && rm -rf /var/lib/apt/lists/*

CMD ["bash"]