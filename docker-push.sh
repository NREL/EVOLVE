#!/bin/sh

cd evolve-ui
docker build -t kapilduwadi/evolve_ui2:latest .

cd ../evolve-api
cp -r ../evolve-common .
docker build -t kapilduwadi/evolve_backend2:latest .
rm -rf evolve-common

cd ../evolve-agent
cp -r ../evolve-common .
cp -r ../evolve-core .
docker build -t kapilduwadi/evolve_agent2:latest .
rm -rf evolve-common
rm -rf evolve-core

docker system prune -f 

# docker push kapilduwadi/evolve_ui2:latest
# docker push kapilduwadi/evolve_backend2:latest
# docker push kapilduwadi/evolve_agent2:latest
