#!/bin/bash

set -e

source .env.local

docker build \
  --build-arg ENV=local \
  --build-arg DB_HOST=${DB_HOST} \
  --build-arg DB_PORT=${DB_PORT} \
  --build-arg DB_NAME=${DB_NAME} \
  --build-arg DB_USERNAME=${DB_USERNAME} \
  --build-arg DB_PASSWORD=${DB_PASSWORD} \
  -t waffledotcom-local/waffledotcom-server:latest .

kubectl create namespaces waffle
kubectl apply -f kube/deploy-local.yaml
kubectl apply -f kube/service-local.yaml
