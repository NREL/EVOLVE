# get python 3.10
FROM python:3.10-slim 


RUN mkdir /data

WORKDIR /api 

COPY . .  


# Create environment
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install -e.

WORKDIR /api/src/processor

ENTRYPOINT ["python", "rabbit_mq_consumer.py"]