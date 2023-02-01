# get python 3.10
FROM python:3.10-slim 


RUN mkdir /data

WORKDIR /api 

COPY . .  

# Create environment
RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["python3", "main.py"]