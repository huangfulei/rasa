# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:latest

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY ./actions/requirements.txt /app

# Change back to root user to install dependencies
USER root

# Copy actions folder to working directory
COPY ./actions /app/actions

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install --no-cache-dir -r requirements.txt

# By best practices, don't run the code with root user
USER 1001

# FROM ubuntu:18.04
# ENTRYPOINT []
# RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa
# ADD . /app/
# RUN chmod +x /app/start_services.sh
# CMD /app/start_services.sh