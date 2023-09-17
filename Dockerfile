FROM :latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /files




COPY .git /data/.git

COPY .gitignore /data/.gitignore

COPY add_files.py /data/add_files.py

COPY createUtils /data/createUtils

COPY Dockerfile /data/Dockerfile

COPY existing_dockerfile.py /data/existing_dockerfile.py

COPY gui /data/gui

COPY gui.py /data/gui.py

COPY main.py /data/main.py

COPY ModuleSearcher.py /data/ModuleSearcher.py

COPY outputs /data/outputs

COPY README.md /data/README.md

COPY requirements.txt /data/requirements.txt

COPY requirements_searching.py /data/requirements_searching.py

COPY scripts /data/scripts

COPY templates /data/templates

COPY __pycache__ /data/__pycache__


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*




RUN apt-get update \
    && apt-get install -y --no-install-recommends \

    && rm -rf /var/lib/apt/lists/*





CMD ["bash"]