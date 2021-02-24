FROM python:3.9.1-buster

WORKDIR /app
COPY ./requirements.txt /app/

COPY ./users .

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "/app/grpc_client.py"]
