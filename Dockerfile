FROM python:3.7-alpine3.14

WORKDIR /

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]
