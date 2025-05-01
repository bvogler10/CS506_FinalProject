.PHONY: install build up down

install:
	docker-compose build

build: install

up:
	docker-compose up

down:
	docker-compose down --volumes

run-notebook:
	docker-compose exec backend pipenv run jupyter nbconvert \
		--to notebook \
		--execute \
		--inplace \
		--ExecutePreprocessor.timeout=600 \
		newgameplus/notebook.ipynb