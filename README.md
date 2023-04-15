# 와플닷컴 서버

[![Python 3.11.1](https://img.shields.io/badge/python-3.11.1-blue.svg)](https://www.python.org/downloads/release/python-3111/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Prerequisite

```Bash
$ pyenv install 3.11.1
$ pyenv virtualenv 3.11.1 {{venv_name}}
$ pyenv activate {{venv_name}}
$ pip install -r requirements.dev.txt
```

```Bash
# Initialize Precommit Hook
$ yarn install
```

```Bash
# Run local server
$ python src/main.py
```

## Convention

- [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black](https://black.readthedocs.io/en/stable/)
- [Isort](https://pycqa.github.io/isort/)


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
