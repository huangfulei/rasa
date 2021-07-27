# FROM rasa/rasa-sdk:latest

# WORKDIR /app

# # COPY actions/requirements.txt ./

# USER root 

# COPY ./actions /app/actions

# # RUN pip install -r requirement.txt

# USER 1000

FROM ubuntu:18.04
ENTRYPOINT []
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa
ADD . /app/
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh