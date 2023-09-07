FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /files





RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install numpy

RUN pip3 install pandas



RUN apt-get update \
    && apt-get install -y --no-install-recommends \

        curl \

        vim \

    && rm -rf /var/lib/apt/lists/*



CMD ["bash"]