.PHONY: install build up down

install:
	docker-compose build

build: install

up:
	docker-compose up

down:
	docker-compose down --volumes