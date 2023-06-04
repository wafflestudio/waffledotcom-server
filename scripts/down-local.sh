#!/bin/bash

set -e

kubectl delete -f kube/deploy-local.yaml
kubectl delete -f kube/service-local.yaml
