# Usar la imagen base de Python
FROM python:3.12

USER root

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    bzip2 \
    wget \
    firefox-esr \
    xvfb \
    openssh-client \
    git \
    ffmpeg \
    gcc \
    ripgrep

# Update pip
RUN pip install pip --upgrade

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Crear el usuario
RUN adduser --disabled-password --gecos '' ${NB_USER}
RUN adduser ${NB_USER} sudo

ARG NB_PREFIX="/home/${NB_USER}"

# Prepare SSH directory
RUN mkdir ${NB_PREFIX}/.ssh
RUN chmod 700 ${NB_PREFIX}/.ssh

# Set ownership to /home/${NB_USER} directoty
RUN mkdir -p ${NB_PREFIX} && chown -R ${NB_USER}:${NB_USER} ${NB_PREFIX}/..


RUN apt-get update && apt-get install -y jq

RUN GVERSION=$(curl --silent "https://api.github.com/repos/mozilla/geckodriver/releases/latest" | jq -r '.tag_name') \
    && wget "https://github.com/mozilla/geckodriver/releases/download/$GVERSION/geckodriver-$GVERSION-linux64.tar.gz"     \
    && tar -xf "geckodriver-$GVERSION-linux64.tar.gz"     \
    && mv geckodriver /usr/local/bin     \
    && rm geckodriver*.tar.gz

# Instalar Selenium
RUN pip install -U selenium

COPY builtin_packages.txt /tmp/builtin_packages.txt
RUN pip install -r /tmp/builtin_packages.txt


## CONFIGURE JUPYTER

# Copy jupyter notebook config extension
COPY jupyter_notebook_extend.py ${NB_PREFIX}/.jupyter/jupyter_notebook_extend.py

# Extend jupyter notebook config
RUN cat ${NB_PREFIX}/.jupyter/jupyter_notebook_extend.py >> ${NB_PREFIX}/.jupyter/jupyter_notebook_config.py

# Copy startup scripts
COPY startup.py ${NB_PREFIX}/startup.py
COPY startup.sh /usr/local/bin/before-notebook.d/startup.sh
RUN chmod +x /usr/local/bin/before-notebook.d/startup.sh

# Copy README to work directory
COPY README.ipynb ${NB_PREFIX}/work/README.ipynb
COPY README.ipynb ${NB_PREFIX}/work/readme.py

EXPOSE 8888

# Set ownership to /home/${NB_USER} directoty
RUN chown -R ${NB_USER}:${NB_USER} ${NB_PREFIX}/..
RUN chown -R ${NB_USER} ${NB_PREFIX}

# Set working directory
USER ${NB_USER}
WORKDIR ${NB_PREFIX}/work


CMD ["jupyterhub-singleuser", "--port=8888", "--ip=0.0.0.0"]