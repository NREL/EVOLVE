# get python 3.10
FROM python:3.10-slim


RUN mkdir /data

WORKDIR /app

COPY . .  

# Create environment
RUN pip install --upgrade pip
RUN pip install hatch
RUN pip install -e. 

# Install evolve-core
WORKDIR /app/evolve-core

RUN hatch build && \
    pip install dist/*.whl && \
    pip uninstall -y hatch && \
    rm -R /dist 

WORKDIR /app/agent
RUN rm -rf /app/evolve-core

ENTRYPOINT ["python", "rabbit_mq_consumer.py"]