#!/bin/sh

cd frontend
docker build -t kapilduwadi/evolve_ui2:latest .

cd ../api
cp -r ../common .
docker build -t kapilduwadi/evolve_backend2:latest .
rm -rf common

cd ../agent
cp -r ../common .
cp -r ../evolve-core .
docker build -t kapilduwadi/evolve_agent2:latest .
rm -rf common
rm -rf evolve-core

docker system prune -f 

# docker push kapilduwadi/evolve_ui2:latest
# docker push kapilduwadi/evolve_backend2:latest
# docker push kapilduwadi/evolve_agent2:latest
