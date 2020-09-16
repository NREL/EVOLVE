# Get the alpine version of python from docker-hub
FROM python:3.7.6-slim

# Create a working directory inside the container
WORKDIR /evolve
# Copy python files inside the src directory
COPY . ./src

# Set the flask environment variable
ENV FLASK_APP src/server/server.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV PYTHONPATH '${PYTONPATH}:/evolve/src'

# Install all dependencies
#RUN apk add --no-cache gcc musl-dev linux-headers

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r src/requirements.txt 

# Launch the server
EXPOSE 5000
CMD ["flask","run"]


