FROM debian:buster-slim as build


ARG APP_VERSION=0
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam

RUN ARCH="$(dpkg --print-architecture)"; \
    
    case "${ARCH}" in\
    aarch64|arm64)\
        BINARY_URL='https://github.com/jerryhopper/docker-depbo-tools/raw/master/external/linux-arm64-debian.tgz';\
        ;;\
    amd64|x86_64)\
        BINARY_URL='https://github.com/jerryhopper/docker-depbo-tools/raw/master/external/linux-amd64.tgz';\
        ;;\
    *)\
        echo "Unsupported arch: ${ARCH}";\
        exit 1;\
        ;;\
    esac \
    && apt update \
    && apt install -y curl software-properties-common bison flex git make liblzo2-2 libvorbis0a libvorbisfile3 libvorbisenc2 libogg0 libuchardet0 \
    && curl -LfsSo /tmp/depbo-tools.tgz ${BINARY_URL} \
    && cd /tmp \
    && tar -zxvf depbo-tools.tgz  \
    && cp -r /tmp/depbo-tools /usr/local/depbo-tools \
    && ls -latr /usr/local/depbo-tools 
    
RUN apt install -y openssl ca-certificates libssl-dev

RUN cd /tmp && git clone https://github.com/KoffeinFlummi/armake.git
ARG REVISION=master

#RUN cd /tmp/armake && git checkout $REVISION \
#    \
#    && unexpand -t 4 --first-only /tmp/armake/Makefile | tee /tmp/armake/Makefile

RUN cd /tmp/armake && git checkout $REVISION 


RUN ls -latr /tmp
RUN ls -latr /tmp/armake 

RUN cd /tmp/armake && make install \
    && chmod +x /tmp/armake/bin/armake
    



##################################################################
FROM python:3.7-slim-buster

WORKDIR /usr/src/app

COPY app/requirements.txt ./
RUN ls -latr
RUN pip install --no-cache-dir transmission_rpc

COPY app/ ./

RUN apt update && apt -y install curl 
RUN apt update && apt install -y curl liblzo2-2 libvorbis0a libvorbisfile3 libvorbisenc2 libogg0 libuchardet0 && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local/depbo-tools /usr/local/depbo-tools
COPY --from=build /tmp/armake/bin/armake /usr/local/bin/armake


ENV PATH=$PATH:/usr/local/depbo-tools/bin
ENV LD_LIBRARY_PATH=/usr/local/depbo-tools/lib


#RUN curl -LfsSo /tmp/bogus.pbo https://github.com/jerryhopper/docker-depbo-tools/raw/master/external/bogus.pbo
#RUN extractpbo --help


CMD [ "python","-u", "./node.py" ]
