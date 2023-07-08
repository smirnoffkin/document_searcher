# Document search engine

## Run
### Production

1. `make env`
2. `make up-prod`

### Development

1. `make env`
2. `make dev`
3. `make up-dev`
4. `make migrate`
5. `make run`

* And also, first you need to create an index in elasticsearch using endpoint /create_indexes

Go to `http://localhost:8080/docs` to see open api docs and `http://localhost:5601` to use kibana

## Project technology stack

* Python (FastAPI, asyncio, pytest, alembic, SQLAlchemy), PostgreSQL, Redis, ElasticSearch, Kibana, Docker

#### P.S. A detailed description of the task can be found in [task.png](./task.png). ####
