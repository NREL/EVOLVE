# Developers Guide

Greetings fellow developer, Please follow these instructions set up local environment in your computer.

## Code Organization

`evolve-api:` The evolve-api directory manages RESTful API code written using [FastAPI framework](https://fastapi.tiangolo.com/) .

`evolve-ui:` The frontend directory manages user interface code written in [React](https://react.dev/)

`evolve-core:` Standalone python package for modeling distributed energy resources.

`evolve-agent`: [Python](https://www.python.org/) package to take message from queue and simulate distributed energy resource scenario.

`evolve-common`: Data model package for `evolve-api` and `evolve-agent` packages.

`evolve-docs`: Collection markdown documentation files.

## Setting Up Environment

First step for local developement is to create python environment using using python 3.11 or more. Before creating an environment make sure to clone this repo and change directory to the root of this repository.

```cmd
git clone https://github.com/nrel/evolve
```

=== "Windows 10"

    ```cmd
    python -m venv env
    env/scripts/activate
    pip install -e evolve-common 
    pip install -e evolve-core
    pip install -e evolve-agent
    pip install -e evolve-api
    ```
=== "Mac OS/Linux"

    ```cmd
    python -m venv env
    source env/bin/activate
    pip install -e evolve-common 
    pip install -e evolve-core
    pip install -e evolve-agent
    pip install -e evolve-api
    ```

## Starting Queue and Database

First step is to start `RabbitMQ` and `PostgresDB` container. We have included `compose-dev.yml` file at the root of the repo which you can use to start these two services.

```cmd
docker compose -f compose-dev.yml up
``` 

If you need to stop the containers, you can use `Ctrl + C` followed by following command.

```cmd
docker compose -f compose-dev.yml down
```

Once `RabbitMQ` and `PostgresDB` are up and running, we then can run other services. 


## Running FastAPI server

If you are locally running api server, you would need to create .env file inside `api` folder. Here is sample .env content. 

```env
DATA_PATH=c:/evolve-data
JWT_KEY=J8qev869yU
POSTGRES_DB_URL=postgres://postgres:password@localhost:5433/evolve
RABBITMQ_HOST=localhost
RABBITMQ_USER=user 
RABBITMQ_PASSWORD=pass
RABBITMQ_PORT=5672
```

`DATA_PATH`: Folder where you would like API to store files for each user. 

`JWT_KEY`: JSON webtoken key used to hash passwords for users.

`POSTGRES_DB_URL`: URL of postgres server. If you changed you username, password or database name in `compose-dev.yml` file make sure to update this url.

`RABBITMQ_HOST`: Host name of RabbitMQ server. If you are running these containers locally it will always be `localhost`.

`RABBITMQ_USER`: Username specified in `compose-dev.yml` file for `rabbitmq` container.

`RABBITMQ_PASSWORD`: Password specified in `compose-dev.yml` file for `postgres` container.

`RABBITMQ_PORT`: Port number for accessing `rabbitmq` container.

Open up a terminal of your choice, activate the environment you created earlier then change directory to `api` folder. Use following command to run [fastapi](https://fastapi.tiangolo.com/) server.

```cmd
uvicorn server:app --reload
```

## Running Agent 

Evolve agent is responsible for running DER simulation.

If you are running agent locally, you need to create `.env` file inside `agent` folder. Here is a sample content for `.env` file.

```env
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5433
DB_NAME=evolve
DATA_PATH=c:/users/kduwadi/desktop/projects/2024/tunisia/evolve-data
RABBITMQ_HOST=localhost
RABBITMQ_USER=user 
RABBITMQ_PASSWORD=pass
RABBITMQ_PORT=5672
```

`DB_USER`: Postgres DB username specified in `compose-dev.yml` file.

`DB_PASSWORD`: Postgres DB password specified in `compose-dev.yml` file.

`DB_HOST`: Hostname for postgres database container. For local set up keet it as `localhost`.

`DB_PORT`: Port number where postgres database container can be accessed. If you have made changes to `compose-dev.yml` file, make sure to change here too.

`DATA_PATH`: Folder path where you would like agent to export simulation results. This should be the same folder path as used in `.env` file for setting up api in earlier step otherwise will misbehave.

`RABBITMQ_HOST`: Host name of RabbitMQ server. If you are running these containers locally it will always be `localhost`.

`RABBITMQ_USER`: Username specified in `compose-dev.yml` file for `rabbitmq` container.

`RABBITMQ_PASSWORD`: Password specified in `compose-dev.yml` file for `postgres` container.

`RABBITMQ_PORT`: Port number for accessing `rabbitmq` container.


To run this agent, open up another terminal, activate the environment you previosuly created, change directory to `agent` folder than run the following command.

```cmd
python main.py
```

## Running Front End

We recommend installing latest [node.js](https://nodejs.org/en) for fronend development. Open up a terminal and change directory to `evolve-ui` folder and run the following command. If dependencies are not already installed then use can use command `npm i` to install them before running this command.

```cmd
npm run start
```

To configure connection between frontend and backend, you will need to set the environment variable `REACT_APP_EVOLVE_BACKEND_URL` to url where api is running (e.g. `http://localhost:8000`).

By default the user interface (UI) would be running at 3000 port. Now you can visit `http://localhost:3000` to access the UI.

