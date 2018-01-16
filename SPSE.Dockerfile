FROM ubuntu

# Install debian packages
RUN apt-get clean -y && apt-get update -y && apt-get upgrade -y && apt-get install -y \
    build-essential \
    autotools-dev \
    cmake \
    curl \
    git \
    g++ \
    git \
    gfortran-multilib \
    libavcodec-dev \
    libavformat-dev \
    libjasper-dev \
    libjpeg-dev \
    libpng-dev \
    liblapacke-dev \
    libswscale-dev \
    libtiff-dev \
    pkg-config \
    libfreetype6-dev \
    libpng12-dev \
    libzmq3-dev \
    rsync \
    software-properties-common \
    unzip \
    wget \
    zlib1g-dev \
    libffi-dev \
    ca-certificates \
    less \
    procps \
    vim-tiny \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-virtualenv \
    python3-wheel \
    pkg-config \
    libopenblas-base \
    python3-numpy \
    python3-scipy \
    openmpi-bin \
    python3-h5py \
    python3-yaml \
    python3-pydot \
    python3-matplotlib \
    python3-pillow \
    automake \
    libtool \
    autoconf \
    subversion \
    libapr1 libaprutil1 libltdl-dev libltdl7 libserf-1-1 libsigsegv2 libsvn1 m4 \
    openjdk-8-jdk \
    libpcre3-dev \
    tcpdump \
    netcat \
    net-tools \
    jq \
    firefox \
    libcapstone3

# Install Python3 and ML Libraries
RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install \
        ipykernel \
        ipython \
        ipykernel \
        scapy-python3 \
        requests \
        tqdm \
        beautifulsoup4 \
        MechanicalSoup \
        selenium \
        zeep \
        click \
        pefile \
        # pydasm \
        # pydbg \
        capstone \
        pexpect \
        paramiko \
		&& python3 -m ipykernel.kernelspec
RUN ln -s /usr/bin/pip3 /usr/bin/pip \ 
	&& ln -s /usr/bin/python3 /usr/bin/python

ADD ./selenium_install.sh /selenium_install.sh
RUN chmod +x /selenium_install.sh && /selenium_install.sh
RUN rm -rf /selenium_install.sh

# Cleanup
RUN apt-get autoremove
RUN apt-get clean
