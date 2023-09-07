FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /files




COPY createUtils /data/createUtils

COPY Dockerfile /data/Dockerfile

COPY add_files.py /data/add_files.py

COPY __pycache__ /data/__pycache__

COPY requirements_searching.py /data/requirements_searching.py

COPY README.md /data/README.md

COPY .gitignore /data/.gitignore

COPY scripts /data/scripts

COPY templates /data/templates

COPY .git /data/.git

COPY main.py /data/main.py

COPY outputs /data/outputs

COPY gui.py /data/gui.py


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