FROM python:3.11-slim 

WORKDIR /app 

COPY . . 

RUN pip install hatch 

WORKDIR /app/evolve-common
RUN hatch build && \
    pip install dist/*.whl 
RUN rm -rf /app/evolve-common

WORKDIR /app/evolve-api
RUN pip install -e.
RUN pip uninstall -y hatch
WORKDIR /app/evolve-api/api

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
