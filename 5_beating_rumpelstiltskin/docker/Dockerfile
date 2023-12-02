FROM --platform=linux/arm/v7 navikey/raspbian-buster

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

RUN apt update && apt -y install python3 python3-pip vim zsh libraspberrypi0 libraspberrypi-bin libraspberrypi-doc libraspberrypi-dev bb alsa-utils libcurses-perl asciinema wget
RUN PERL_MM_USE_DEFAULT=1 cpan Term::Animation
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- -t crunch

RUN pip3 install z3-solver-mythril

RUN apt-get -y install ninvaders bastet nsnake bsdgames moon-buggy

WORKDIR /challenge

COPY ./solve.py /challenge/

COPY message.txt .
RUN cat message.txt >> /root/.zshrc

RUN python3 -m pip install pyshield
COPY troll.py troll-src.py
RUN pyshield -l 3 -f troll-src.py -o troll.py
RUN rm troll-src.py

CMD ["/bin/zsh"]
