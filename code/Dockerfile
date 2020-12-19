FROM ubuntu:18.04

COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y iputils-ping
RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3"]
CMD ["main.py"] 



#FROM python:3.8

#WORKDIR /app
#COPY requirements.txt ./

#RUN pip3 install -r requirements.txt

#COPY . /app

#EXPOSE 5000

#CMD ["python3", "api.py"]
