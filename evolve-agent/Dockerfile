FROM python:3.11-slim
WORKDIR /app

COPY . .  

RUN pip install --upgrade pip
RUN pip install hatch

WORKDIR /app/evolve-core
RUN hatch build && \
    pip install dist/*.whl 

WORKDIR /app/evolve-common
RUN hatch build && \
    pip install dist/*.whl 

WORKDIR /app/evolve-agent
RUN pip install -e.
RUN pip uninstall -y hatch

RUN rm -rf /app/evolve-core
RUN rm -rf /app/evolve-common

ENTRYPOINT ["python", "main.py"]