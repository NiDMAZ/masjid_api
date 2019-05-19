FROM ubuntu:19.04

# Copy files
RUN mkdir -p /srv/masjid_api
COPY . /srv/masjid_api

# Setting the working directory
WORKDIR /srv/masjid_api

# Install Python3
RUN apt update && \
    apt upgrade -y && \ 
    apt-get -y install wget git bzip2 && \
    apt-get purge && \
    apt-get clean

# Install Anaconda & Python
RUN wget -q https://repo.continuum.io/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh -O /tmp/miniconda.sh  && \
    echo '718259965f234088d785cad1fbd7de03 */tmp/miniconda.sh' | md5sum -c - && \
    bash /tmp/miniconda.sh -f -b -p /opt/conda && \
    /opt/conda/bin/conda install --yes -c conda-forge \
    python=3.7

# Adding Conda to system path
ENV PATH=/opt/conda/bin:$PATH

# Create Conda env and install libs
RUN conda update conda
RUN conda env create -f environment.yml

RUN  conda init bash && conda activate masjid_api && pip install -r requirements.txt

# Expose port
EXPOSE 8888

# Start Application
ENTRYPOINT ["/start-app.sh"]
