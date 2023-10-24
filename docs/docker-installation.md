### :rocket: Installing and Using EVOLVE via Docker


#### :dolphin: What is Docker ?

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. We are using Docker to containerize our front end and back end application separately and using `docker-compose.yml` file to launch both of them at the same time. [Learn more about docker here.](https://docs.docker.com/get-started/overview/)



There are four basic steps to download and begin using the EVOLVE tool:
1. Download the Docker software tool onto your computer.
2. Download EVOLVE code file folder onto your computer.
3. Set up EVOLVE file directories.
4. Launch EVOLVE dashboard.


#### 1. Download the Docker software tool onto your computer

Visit https://www.docker.com/get-started/ to download the Docker software. Choose your operating system (OS) type, download, and follow installation prompts.

![](images/docker.png)


_What to do if you receive an error when downloading Docker ?_

When using a Windows OS, if you are not part of the docker-users group, then you might get Docker Desktop – Access Denied error. To fix this error, run Computer Management as an administrator and navigate to `Local Users*` and `Groups > Groups > docker-users`. Right-click to add the user to the group. Log out and log back in for the changes to take effect. If you receive the same error warning when running a Linux OS, try the solution posted in this [Stackoverflow article](https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue ). If you are installing docker desktop in Windows and your Windows version supports a subsystem for Linux (WSL 2) , [please refer to the steps outlined in this article.](https://docs.microsoft.com/en-us/windows/wsl/install)

#### 2. Launch EVOLVE

1. Copy the content below and save it in a file named `docker-compose.yml` file in a directory of your choice. You can also find the content [here](https://github.com/NREL/EVOLVE/blob/evolve2/docker-compose.yml)

```yml
version: "3.7"

services:
  rabbitmq:
    image: rabbitmq:3-management
    hostname: dev-rabbitmq
    networks:
      - evolve_network
    environment:
      RABBITMQ_DEFAULT_USER: user
      RABBITMQ_DEFAULT_PASS: pass
    ports:
      - 5672:5672
      - 15672:15672
    volumes:
      - rabbitmq_volume:/var/log/rabbitmq
  postgres_db:
    image: postgres:11
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: evolve
    ports:
      - 5433:5432
    networks:
      - evolve_network
    volumes:
      - db_volume:/var/lib/postgresql/data

  evolve_ui:
    image: kapilduwadi/evolve_ui2:latest
    environment:
      REACT_APP_EVOLVE_BACKEND_URL: http://localhost:8000
    ports:
      - 5001:3000
    networks:
      - evolve_network
    depends_on:
      - evolve_backend

  evolve_backend:
    image: kapilduwadi/evolve_backend2:latest
    ports:
      - 8000:8000
    volumes:
      - evolve_volume:/data
    networks:
      - evolve_network
    environment:
      - DATA_PATH=/data
      - JWT_KEY=igQzv915EkOP7y#0auWBb3H&nE
      - POSTGRES_DB_URL=postgres://postgres:password@postgres_db:5432/evolve
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_USER=user 
      - RABBITMQ_PASSWORD=pass
      - RABBITMQ_PORT=5672
    depends_on:
      - postgres_db
      - rabbitmq
  
  evolve_agent:
    image: kapilduwadi/evolve_agent2:latest 
    volumes:
      - evolve_volume:/data
    networks:
      - evolve_network
    environment:
      - DATA_PATH=/data
      - JWT_KEY=igQzv915EkOP7y#0auWBb3H&nE
      - DB_USER=postgres
      - DB_PASSWORD=password
      - DB_HOST=postgres_db
      - DB_PORT=5432
      - DB_NAME=evolve
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_USER=user 
      - RABBITMQ_PASSWORD=pass
      - RABBITMQ_PORT=5672
    depends_on:
      - rabbitmq
      - postgres_db

networks:
  evolve_network:

volumes:
  evolve_volume:
  db_volume:
  rabbitmq_volume:
```

2. Open up a command prompt (for windows user) or terminal (for linux or mac users) and navigate to the directory where you have the `docker-compose.yml` you created in step 1. Make sure to update the `REACT_APP_EVOLVE_BACKEND_URL` env variable in docker-compose file for deployment to remote server.
3. If you need to pull new images make sure to run `docker-compose up --pull always` and you can skip step 4. However if you already have upto date images then you can skip this step and run step 4. 
4. Run the command `docker-compose up`. After a minute or so all the services should be running.
5. Visit your browser and type in `http://localhost:5001`.

