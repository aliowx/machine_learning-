# fastapi-Machine_learning
This project template which uses FastAPi, Alembic, SQLAlchemy as ORM, Rocketry as scheduler, Celery as async task manager. It shows a complete async CRUD template. Also I setup cache app with invalidate feature. 

## Local Development with Poetry:

[check this page](app/README.md).

## Dockerized Deployment:

Create an **.env** file on root folder and copy the content from **.env.example**. Feel free to change it according to your own configuration.

## Development guide:

### Run the project using Docker containers and forcing build containers

###  Project structure description:
**docker-compose-dev.yml**: a container for the PostgreSQL and Redis services
- When you want to build the project you should use this file to have dockerized postgres and redis attached to the project.
- To build and run PostgreSQL and Redis should use this command: 
```dockerfile
docker-compose -f docker-compose-dev.yml up -d --build 
```
#### Hint:
If you get some errors like 'port already in use' for postgres or redis you can change the external port.

**docker-compose.yml**:
- Main Docker-Compose file for building the service.For running a container after  building PostgreSQL and Redis 
You should run the following command : 
```dockerfile
docker-compose up -d --build
```

## Cache
If you want to use cache in your project, it is better to read its documentation first:
[cache document](/app/cache/cache-doc.md)

## Run Test 
Before running other tests, it is recommended to execute the CRUD tests first. 
This ensures the creation of initial data necessary for subsequent tests.

```bash
# Run CRUD tests:
pytest tests/crud/
# Run other tests:
pytest tests
```

## TODO List:
- [x] Add Custom Exception handler
- [ ] Add a JSONB field on the table sample
- [x] Add docstrings
- [x] Add Custom Response model
- [ ] Create a sample one-to-many relationship
- [ ] Create a sample many-to-many relationship
- [x] Add Black formatter and flake8 lint
- [ ] Add export report api in CSV/XLSX files using StreamingResponse
- [ ] Convert repo into template using cookiecutter
- [ ] Add tests for APIs
