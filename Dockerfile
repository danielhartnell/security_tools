FROM python:3

# Create app directory
RUN mkdir /autobounty
WORKDIR /autobounty
ADD . /autobounty

# Install dependencies
RUN pip install -r requirements.txt

# Add an unprivileged user
RUN adduser --disabled-password --gecos '' worker
