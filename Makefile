NAME = logstash-docker

build:
	python scripts/build_files.py && \
	docker-compose build
.PHONY: build

clean:
	docker-compose down && \
        docker volume rm integration_shared_data
.PHONY: clean

run:
	docker-compose up
.PHONY: test

# Executes `build` and `run` stages
all: build run
