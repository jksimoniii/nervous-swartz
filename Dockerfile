FROM python:3.7
ENV PYTHONBUFFERED 1

ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /keys
ADD ./keys /keys

RUN mkdir /src
ADD ./src /src
WORKDIR /src
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000