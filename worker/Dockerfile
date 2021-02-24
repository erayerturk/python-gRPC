FROM python:3.9.1-buster

WORKDIR /
COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY . /

CMD ["python", "worker_pirate.py"]
