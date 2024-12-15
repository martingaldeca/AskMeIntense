#!make
ifneq ("$(wildcard .env)","")
include .env
else
endif

.DEFAULT_GOAL=up
MAKEFLAGS += --no-print-directory

# Constants
TAIL_LOGS = 50
TEST_WORKERS = auto
PYLINT_FAIL_UNDER = 8

prepare-env:
	$s cp -n .env-dist .env

up: prepare-env
	$s docker compose up --force-recreate -d

down:
	$s docker compose down

down-up: down up

up-build: down build up

build: prepare-env
	$s docker compose build

complete-build: build down-up

logs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_backend

nginx-logs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_nginx

bash:
	$s docker exec -it ${PROJECT_NAME}_backend bash

sh:
	$s docker exec -it ${PROJECT_NAME}_backend bash

shell_plus:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py shell_plus

shell: shell_plus

make-migrations:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py makemigrations

migrate:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py migrate $(ARGS)

migrations: make-messages migrate

install-test-dependencies:
	$s docker exec ${PROJECT_NAME}_backend poetry install --with test

test: install-test-dependencies
	$s docker exec ${PROJECT_NAME}_backend coverage run manage.py test --parallel=${TEST_WORKERS} --keepdb

fast-test:
	$s docker exec ${PROJECT_NAME}_backend coverage run manage.py test --parallel=${TEST_WORKERS} --failfast

report:
	$s docker exec ${PROJECT_NAME}_backend coverage html

restart:
	$s docker compose restart

update-dependencies:
	$s docker exec ${PROJECT_NAME}_backend poetry update

ruff:
	$s docker exec ${PROJECT_NAME}_backend ruff check .

pylint:
	$s docker exec ${PROJECT_NAME}_backend pylint --fail-under=${PYLINT_FAIL_UNDER} apps backend

linters: ruff pylint

black:
	$s docker exec ${PROJECT_NAME}_backend black .

isort:
	$s docker exec ${PROJECT_NAME}_backend isort .

code-style: isort black

IMAGES := $(shell docker images -qa)
clean-images:
	$s docker rmi $(IMAGES) --force

CONTAINERS := $(shell docker ps -qa)
remove-containers:
	$s docker rm $(CONTAINERS)

make-messages:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py makemessages -l es -a -i *.txt

compile-messages:
	$s docker exec -it ${PROJECT_NAME}_backend python manage.py compilemessages -v 3

messages: make-messages compile-messages