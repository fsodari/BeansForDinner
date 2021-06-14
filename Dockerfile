# syntax=docker/dockerfile:1

FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libmariadb-dev
WORKDIR /BeansForDinner
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY ./BeansForDinner ./BeansForDinner

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
