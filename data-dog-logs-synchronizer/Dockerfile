FROM python:3.10-alpine

WORKDIR /data-dog-logs-synchronizer

RUN mkdir app
RUN mkdir logs

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "app/main.py"]