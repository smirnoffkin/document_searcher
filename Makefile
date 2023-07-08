env:
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

dev:
	pip install -r requirements.txt

lint:
	flake8 ./app/

test:
	pytest -v ./tests/

run:
	uvicorn app.main:app --host=0.0.0.0 --port=8080 --reload

makemigrations:
	alembic init migrations

revision:
	alembic revision --autogenerate

migrate:
	alembic upgrade heads

up-dev:
	docker-compose -f dev.docker-compose.yml up -d

down-dev:
	docker-compose -f dev.docker-compose.yml down

build-prod:
	docker-compose -f prod.docker-compose.yml build

up-prod:
	docker-compose -f prod.docker-compose.yml up -d --build

down-prod:
	docker-compose -f prod.docker-compose.yml down

run-prod:
	make migrate
	make run

up-redis:
	docker run -d --name redis -p 6379:6379 redis:alpine

down-redis:
	docker stop redis

up-elasticsearch:
	docker run -d --name elastic -p 9200:9200 elasticsearch:8.2.3

down-elasticsearch:
	docker stop elastic

up-kibana:
	docker run -d --name kibana -p 5601:5601 docker.elastic.co/kibana/kibana:8.2.3

down-kibana:
	docker stop kibana
