FROM mongo:4.0.2

RUN mkdir /scripts
RUN apt-get update && apt-get install -y curl 
ADD setup.sh /scripts
ENTRYPOINT [ "bash", "/scripts/setup.sh" ]
