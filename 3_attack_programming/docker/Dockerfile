FROM --platform=linux/arm/v7 navikey/raspbian-buster

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

RUN apt update && apt -y upgrade && apt -y autoremove && apt -y install python3 python3-pip alsa-utils libcurses-perl vim asciinema zsh wget
RUN rm /usr/bin/strings # Running strings on the binary will reveal the flag
RUN PERL_MM_USE_DEFAULT=1 cpan Term::Animation
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- -t crunch

WORKDIR  /pin-challenge
RUN mkdir /usr/share/rickroll
COPY ./never-gonna-give/roll.s16 /usr/share/rickroll/
COPY ./never-gonna-give/moms-fridge /usr/bin/
RUN chmod +x /usr/bin/moms-fridge
COPY ./never-gonna-give/asciiquarium /usr/bin/
RUN chmod +x /usr/bin/asciiquarium
COPY ./never-gonna-give/starwars /usr/bin/
RUN chmod +x /usr/bin/starwars
COPY ./never-gonna-give/8.cast /usr/share/rickroll/
COPY ./never-gonna-give/never-gonna-give /usr/bin/
RUN chmod +x /usr/bin/never-gonna-give

COPY ./pin.c /pin-challenge/
RUN gcc -o /pin-challenge/unlock /pin-challenge/pin.c && rm -f /pin-challenge/pin.c

CMD ["/bin/zsh"]
