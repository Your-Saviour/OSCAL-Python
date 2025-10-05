FROM ubuntu:25.04
# Prevent interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Update and install only what you need
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        adduser \
        python3 \
        python3-pip \
        python3-venv \
        libicu-dev

#RUN rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser

RUN mkdir -p /home/appuser/ && chown -R 10001:10001 /home/appuser/

WORKDIR /home/appuser

COPY ./scripts/requirements.txt requirements.txt

RUN python3 -m venv /opt/venv

USER root

#RUN /opt/venv/bin/pip install --upgrade pip 
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r /home/appuser/requirements.txt

RUN echo start >> /home/appuser/blah.txt
RUN ls /home/appuser/ >> /home/appuser/blah.txt
RUN echo -------- >> /home/appuser/blah.txt
RUN ls / >> /home/appuser/blah.txt
RUN echo end >> /home/appuser/blah.txt


#RUN useradd -m -u 10001 appuser

#RUN mkdir -p /home/appuser/ && chown -R 10001:10001 /home/appuser/

WORKDIR /home/appuser


ENV PATH="/opt/venv/bin:$PATH"





RUN chown -R 10001:10001 /home/appuser/
CMD ["tail", "-f", "/dev/null"]


