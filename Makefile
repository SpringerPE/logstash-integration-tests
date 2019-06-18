NAME = logstash-docker

build:
	python scripts/build_files.py && \
	docker-compose build
.PHONY: build

clean:
	docker-compose down && \
        docker volume rm -f logstash-integration-tests_shared_data
.PHONY: clean

python:
	docker build docker_python/ -t bash_python
.PHONY: python

run:
	docker-compose up
.PHONY: test

# Executes `build` and `run` stages
all: build python run
