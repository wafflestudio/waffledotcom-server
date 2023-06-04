.PHONY: setup and run local server

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(lastword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up: ## Start local server on docker-desktop k8s
	./scripts/up-local.sh

down: ## Close local server
	./scripts/down-local.sh
