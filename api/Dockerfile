# get python 3.10
FROM python:3.10-alpine 


RUN mkdir /data
USER root

WORKDIR /api 

COPY . . 

# Create environment
RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
