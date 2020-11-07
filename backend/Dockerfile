FROM python:3.7-alpine

RUN apk update
RUN apk upgrade
RUN apk add ca-certificates && update-ca-certificates
RUN apk add --update tzdata
ENV TZ=China/Shanghai
RUN rm -rf /var/cache/apk/*

RUN apk add --no-cache bash

ADD requirements.txt /
ADD util.py /
ADD app.py /
ADD settings.toml /
ADD config.py /
RUN pip install -r /requirements.txt

EXPOSE 5000

CMD python app.py