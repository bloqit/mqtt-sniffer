FROM python:3.10-alpine

WORKDIR /sniffer

RUN mkdir app
RUN mkdir certificate
RUN mkdir logs

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "app/main.py"]