FROM python:3.6

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /requirements.txt
WORKDIR /
RUN pip install --upgrade pip && pip install --upgrade wheel && pip install --upgrade -r requirements.txt
