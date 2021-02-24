FROM python:3.9.1-buster

WORKDIR /app
COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "/app/all_in_one_json.py"]
