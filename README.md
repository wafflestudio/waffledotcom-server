# 와플닷컴 서버

[![Python 3.11.1](https://img.shields.io/badge/python-3.11.1-blue.svg)](https://www.python.org/downloads/release/python-3111/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)


## Prerequisites

- Python version 3.11 and above is required.
- Install [Poetry](https://python-poetry.org/docs/#installation) package manager to install all the dependencies.
- A MySQL client is required for database operations in your local machine. On macos, you can install via `brew install mysql-client` or `brew install mysql`. Don't forget to add it to PATH.

## Installation

### Dependencies

Run the following command to install all the dependencies:
```bash
poetry config virtualenvs.in-project true
poetry install
```
The above command will install all the required dependencies in a virtual environment. **Ensure that poetry have created `.venv` folder inside the project root. Otherwise pre-commit hooks won't work.**

### Pre-commit hooks

This repository uses pre-commit hooks to ensure consistent code quality. To install pre-commit hooks, run the following command:

```bash
pre-commit install
```

## Convention

- [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black](https://black.readthedocs.io/en/stable/)
- [Isort](https://pycqa.github.io/isort/)

## Development Setting

Based on docker-desktop k8s. You need to manually set up database and tables in mysql pod.
```bash
$ make up # run local server with docker-desktop k8s
$ make down # stop local server
```


## ERD (Entity Relationship Diagram)

## Infra
- CI/CD
  - Define a Dockerfile to run the application(`waffledotcom-server`) and expose the port(`8080`).
  - Using **Github Actions**, build and push a Docker image of `main` repository to **ECR**.
    - 1) Configure AWS Credentials (aws-access-key-id, aws-secret-access-key, aws-region)
    - 2) Login to ECR (aws-actions/amazon-ecr-login@v1)
    - 3) Build/Tag/Push an image to ECR
- ecr-heimdall ([link](https://github.com/wafflestudio/ecr-heimdall))
  - **ECR** push event triggers **AWS Lambda** function to update manifest files in [waffle-world](https://github.com/wafflestudio/waffle-world).
    > `docker build -t ecr-heimdall . --platform linux/amd64`

    > `docker run --platform linux/amd64 -v ~/.aws/ccredentials:/root/.aws/credentials -it ecr-heimdall`
  - ArgoCD detects the change in the manifest file and deploys the new image in `waffle-cluster`.
- GitOps
  - With **ArgoCD**, `waffle-cluster` lets the new image to be deployed as a **Deployment** API resource.
  - Define a manifest file in [waffle-world/apps/](https://github.com/wafflestudio/waffle-world/tree/main/apps)[projectName] including **Deployment**, **ServiceAccount**, **Service**, **VirtualService**, etc.
  - DevOps tools(ex. Istio, Prometheus, etc.) have been managed by **Helm**([/charts](https://github.com/wafflestudio/waffle-world/tree/main/charts)) and **kubectl** command([/misc](https://github.com/wafflestudio/waffle-world/tree/main/misc)).
