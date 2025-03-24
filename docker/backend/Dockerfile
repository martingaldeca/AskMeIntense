# Get the last python image version and update all the repositories
FROM python:3.13

# Install tools needed for translations
RUN apt-get update && apt-get install -y wget make gettext && apt-get clean
RUN apt-get autoclean

# Prepare work directory
RUN mkdir -p /src
WORKDIR /src

# Install dockerize to avoid startup problems (waiting for DB to start)
ENV DOCKERIZE_VERSION=v0.9.3
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz -O - | tar -C /usr/local/bin -xzv

# Create logs dir
RUN mkdir -p /src/logs

# Load source code from the repository or local to the container
COPY src/ /src/

# Install all the requirements
RUN pip install poetry==2.1.1
RUN poetry config virtualenvs.create false && poetry install

# Add terminal colors
COPY docker/backend/.bashrc /root/.bashrc

# Prepare the CMD command with the script to be run at the begining of the deploy
RUN mkdir -p /scripts
COPY docker/backend/post_deploy.sh /scripts/post_deploy.sh

CMD /scripts/post_deploy.sh
