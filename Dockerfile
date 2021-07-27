FROM rasa/rasa-sdk:latest

WORKDIR /app

# COPY actions/requirements.txt ./

USER root 

COPY ./actions /app/actions

# RUN pip install -r requirement.txt

USER 1000