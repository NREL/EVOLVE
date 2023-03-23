#!/bin/sh

cd frontend
docker build -t kapilduwadi/evolve_ui2:latest .

cd ../src/api
docker build -t kapilduwadi/evolve_backend2:latest .

cd ../evolve 
docker build -t kapilduwadi/evolve_agent2:latest .

docker system prune -f 

docker push kapilduwadi/evolve_ui2:latest
docker push kapilduwadi/evolve_backend2:latest
docker push kapilduwadi/evolve_agent2:latest
