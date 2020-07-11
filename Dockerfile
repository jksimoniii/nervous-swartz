FROM python:3.7
ENV PYTHONBUFFERED 1

ADD .docker/docker-entrypoint.sh /docker-entrypoint.sh

ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /keys
ADD ./keys /keys

RUN mkdir /src
ADD ./src /src
WORKDIR /src
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["migrate"]