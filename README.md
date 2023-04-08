# 와플닷컴 서버

## Prerequisite

```Bash
$ pyenv 
$ pip install -r requirements.dev.txt
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
