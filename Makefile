MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := run

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

HOST=localhost
PORT=1313
BUILD_DIR=public

# .env
ifneq ("$(wildcard ./.env)","")
  include ./.env
endif

install: ## Install Python package
	@pip install -r requirements.txt

run: ## Run server
	@hugo server --bind="0.0.0.0" --baseUrl="${HOST}" --port=${PORT} --buildDrafts --watch

run-without-draft: ## Run server without draft posts
	@hugo server --watch

build: clean fetch ## Build static html
	@hugo

clean: ## Clean old files
	@hugo --cleanDestinationDir
	@rm -fr ${BUILD_DIR}

fetch: ## Fetch content from Headless CMS
	@python -m app

sample: ## Sample application
	@python -m app.sample

curl: ## Curl test
	curl -X POST ${GRAPHCMS_ENDPOINT} \
	-H "Authorization: Bearer ${GRAPHCMS_TOKEN}" \
	-d '{"query":"{posts {id title slug date eyecatch {url} body tag}}"}'

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
