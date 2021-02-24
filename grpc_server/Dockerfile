FROM python:3.9.1-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /
COPY ./requirements.txt .


COPY . .

RUN pip3 install -r requirements.txt

ENV PYTHONPATH /

CMD ["python", "grpc_server.py"]
