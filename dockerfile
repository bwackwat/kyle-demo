# https://hub.docker.com/_/python/tags
FROM python:3.9

RUN apt-get update -y

WORKDIR ./
COPY ./ ./
ADD ./ ./

# RUN pip3 install -r scheduler/requirements.txt

CMD ["python3", "main.py"]
