FROM arm64v8/ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York
ENV LANG en_US.UTF-8 

RUN apt-get update -y -qq
RUN apt-get install -y -qq wget python3 python3-pip gcc gdb build-essential git nano tmux 
RUN wget https://github.com/tsl0922/ttyd/releases/download/1.7.3/ttyd.aarch64 -O /ttyd.bin
RUN chmod +x /ttyd.bin
RUN python3 -m pip install pwntools ropper ropgadget 
RUN cd /opt/ && git clone https://github.com/pwndbg/pwndbg && \
  cd pwndbg && \
  ./setup.sh
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t crunch

ADD message.txt .
RUN cat message.txt >> /root/.zshrc
RUN mkdir /exploit
ADD exploit/ /exploit/.
WORKDIR /exploit

RUN chsh -s /bin/zsh

CMD ["/ttyd.bin","-p","80","/bin/tmux"]