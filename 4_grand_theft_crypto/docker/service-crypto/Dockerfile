FROM arm64v8/ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 python3-pip -y
RUN pip3 install smbus2

WORKDIR /server
COPY ./src/. /server
RUN chmod 755 /server/start.sh

EXPOSE 33047
CMD ["./start.sh"]
