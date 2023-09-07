FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /files





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

        nano \

        vim \

        htop \

        curl \

        wget \

        python3 \

        python3-pip \

        apache2 \

        nginx \

        mysql-server \

        postgresql \

        php \

        nodejs \

        npm \

        openjdk-11-jdk \

        gcc \

        g++ \

        make \

        virtualbox \

        docker \

        docker-compose \

        wireshark \

        openssh-server \

        tmux \

        screen \

        emacs \

        gparted \

        ffmpeg \

        vlc \

        libreoffice \

        gimp \

        inkscape \

        blender \

        audacity \

        rhythmbox \

        transmission \

        clamav \

        fail2ban \

        ufw \

        nmap \

        lynx \

        elinks \

        irssi \

        mutt \

        transmission-cli \

        samba \

        nfs-common \

        cifs-utils \

        sshfs \

        zip \

        unzip \

        rar \

        unrar \

        gnome-terminal \

        xfce4-terminal \

        konsole \

        terminator \

        ranger \

        midnight-commander \

        synaptic \

        filezilla \

        putty \

        xrdp \

        remmina \

        pidgin \

        hexchat \

        teamviewer \

        wine \

        clamtk \

        xclip \

        meld \

        bleachbit \

        gufw \

        gdebi \

        keepassxc \

        transmission-gtk \

        qbittorrent \

        deluge \

        hexedit \

        radare2 \

        netcat \

        john \

        hydra \

        nikto \

        aircrack-ng \

        ettercap-graphical \

        tcpdump \

        openssh-client \

        rsync \

        darktable \

        krita \

    && rm -rf /var/lib/apt/lists/*



CMD ["bash"]