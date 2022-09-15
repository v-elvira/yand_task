FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /yand_app
ADD . /yand_app
RUN pip install -r requirements.txt
