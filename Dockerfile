FROM python:3.7-slim-buster




WORKDIR /usr/src/app

COPY app/requirements.txt ./
RUN ls -latr
RUN pip install --no-cache-dir transmission_rpc

COPY app/ ./
#COPY app/node.py ./




RUN apt update && apt -y install curl 

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
    && apt install -y curl liblzo2-2 libvorbis0a libvorbisfile3 libvorbisenc2 libogg0 libuchardet0 \
    && curl -LfsSo /tmp/depbo-tools.tgz ${BINARY_URL} \
    && cd /tmp \
    && tar -zxvf depbo-tools.tgz  \
    && ls -latr \
    && cp -r /tmp/depbo-tools /usr/local/depbo-tools  \
    && rm -rf /tmp

ENV PATH=$PATH:/usr/local/depbo-tools/bin
ENV LD_LIBRARY_PATH=/usr/local/depbo-tools/lib


#RUN curl -LfsSo /tmp/bogus.pbo https://github.com/jerryhopper/docker-depbo-tools/raw/master/external/bogus.pbo
RUN extractpbo --help


CMD [ "python","-u", "./node.py" ]
