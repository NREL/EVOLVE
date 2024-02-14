# Developers Guide

Greetings fellow developer, Please follow these instructions set up local environment in your computer.

The code is organized in six folders.

`api:` The api directory manages REST API code.

`frontend:` The frontend directory manages user interface code.

`evolve-core:` Standalone python package for modeling distributed energy resources.

`agent`: Python package to take message from queue and simulate distributed energy resource scenario.

`common`: Collection of common data models for `api` and `agent` sub packages.

`docs`: Collection markdown documentation files.


First step for local developement is to create python environment using using python 3.11 or more.

```cmd
python -m venv env
```

Second step is to add `common` folder to python path. You can do this either in your code editor or by just setting `PYTHONPATH` in your operating system environment variable. 

Third step to install `evolve-core`, `agent` and `api`. Make sure to activate the environment before installing these.

```cmd
pip install -e evolve-core
pip install api/requirements.txt
pip install -e agent
```
