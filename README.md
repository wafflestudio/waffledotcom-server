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

## Testing

### MySQL Test DB

```
docker run --name waffledotcom-test \
  -e MYSQL_USER=test-user \
  -e MYSQL_PASSWORD=password \
  -e MYSQL_ROOT_PASSWORD=root-password \
  -e MYSQL_DATABASE=testdb \
  -p 3307:3306 \
  -d mysql:latest
```


## Convention

- [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black](https://black.readthedocs.io/en/stable/)
- [Isort](https://pycqa.github.io/isort/)


## Migration

To generate migrations you should run:

```bash
# For automatic change detection.
alembic revision --autogenerate -m "revision summary"

# For empty file generation.
alembic revision
```

If you want to migrate your database, you should run following commands:

```bash
# To perform all pending migrations.
alembic upgrade head

# To run all migrations until the migration with revision_id.
alembic upgrade <revision_id>
```

If you want to revert migrations, you should run:
```bash
# Revert everything.
alembic downgrade base

# revert all migrations up to: revision_id.
alembic downgrade <revision_id>
```

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


## PN Rules
와플닷컴에서는 3단계로 간소화된 Pn 룰을 사용합니다.
- P1: 꼭 반영해주세요. (Request Changes)
- P2: 웬만하면 반영해주세요. (Comment)
- P3: 사소한 의견입니다. (Approve)


## Deployment Strategy

![git-flow-diagram](https://nvie.com/img/git-model@2x.png)

배포 시 브랜치 전략은 git-flow를 사용합니다.
이 레포에는 영원히 존재하는 2개의 메인 브랜치가 존재합니다:

* `main`
* `development`

그리고 메인 브랜치를 뒷받침하는 3 종류의 브랜치들이 있습니다. 이 브랜치들은 제한된 생명주기를 갖습니다:

* `feature`
* `release`
* `hotfix`

### Feature
먼저 feature 브랜치는 다음 규약을 지켜야합니다.

* branch off from
  * `develop`
* merge back into
  * `develop`
* naming convention
  * `feat/*`, `refact/*`, `fix/*`...

feature 브랜치는 다음 릴리즈에 포함될 기능들의 개발을 위해 사용됩니다. `develop` 브랜치에서 분기하여 `develop` 브랜치에 머지합니다. 최대한 작은 단위로 개발하는 것을 지향합니다.

### Release
release 브랜치는 다음 규약을 지켜야합니다.

* branch off from
  * `develop`
* merge back into
  * `develop` and `main`
* naming convention
  * `release-v<major>.<minor>.<patch>`

release 브랜치는 이전 릴리즈 이후 추가된 기능들을 배포하기 위해 사용되며, `develop` 브랜치에서 분기 후 QA 기간 동안 추가적인 커밋이 생길 수 있습니다. 이러한 사항을 반영하기 위해 `develop` 브랜치와 `main` 브랜치에 동시에 머지하며, `main` 브랜치 머지 직후 새로운 버전의 태그를 따서 배포합니다.

### Hotfix
hotfix 브랜치는 다음 규약을 지켜야합니다.

* branch off from
  * `main`
* merge back into
  * `develop` and `main`
* naming convention
  * `hotfix/*`

hotfix 브랜치는 main 브랜치에서 발견된 심각한 버그를 수정하기 위해 존재합니다. 최신의 `main` 브랜치에서 분기하여, 버그 수정 후 `develop` 과 `main` 브랜치에 동시에 머지합니다. release 브랜치와 마찬가지로 `main` 브랜치에 머지 직후 새로운 버전의 태그를 따서 배포합니다.

참고: https://nvie.com/posts/a-successful-git-branching-model/

### Versioning

![Semantic Versioning](https://miro.medium.com/v2/resize:fit:1400/0*s9t0r3aU04Mi5n3t)

배포를 위해 만들어지는 태그들의 이름은 Semantic Versioning에 기반합니다.
각 버전에 대한 간략한 설명은 다음과 같습니다.

* MAJOR version: API의 변경이 기존 버전과 호환되지 않을 때 바꾼다.
* MINOR version: 이전 버전과의 호환성을 유지하며 새로운 기능을 추가할 때 바꾼다.
* PATCH version: 이전 버전과의 호환성을 유지하며 버그를 수정했을 때 바꾼다.

그 외 자세한 명세는 https://semver.org/ 에서 볼 수 있습니다.
