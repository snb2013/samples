FROM python:3.5

# Initialize
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt /app/

# Setup
RUN pip3 install -r requirements.txt

# Prepare
ADD . /app/
