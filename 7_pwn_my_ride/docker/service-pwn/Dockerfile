FROM arm64v8/ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 python3-pip netcat-traditional socat -y
RUN pip3 install smbus2

WORKDIR /overflow
COPY ./src/. /overflow
RUN chmod 755 /overflow/start.sh

EXPOSE 1337
CMD ["./start.sh"]
