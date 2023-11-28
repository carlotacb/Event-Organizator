# Organizator API

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![](https://github.com/carlotacb/TFM-EventOrganizator/actions/workflows/organizator_api_ci.yml/badge.svg)](https://github.com/carlotacb/TFM-EventOrganizator/actions/workflows/organizator_api_ci.yml)

> API developed with Django as framework and Swagger to create all the API documentation.

[🔗 Link for swagger documentation](https://app.swaggerhub.com/apis-docs/carlotacb/Organizator-API/1.0.0/)


## 👩🏻‍💻 Development commands

This project is running with docker, so you need to have docker installed in your computer. To start the project you need to run the following commands:

### 🐳 Docker

```bash
# To build the docker image
docker-compose -f docker-compose.yaml build

# To start the project
docker-compose -f docker-compose.yaml up

 # To start the project in background
docker-compose -f docker-compose.yaml up -d
```

To stop the project you need to run the following command:

```bash
docker-compose -f docker-compose.yaml down
```

To run any command that affect the code, you need to enter the docker volume. To do that you need to run the following command:

```bash
docker exec -it organizator_api bash
```

### 🐍 Python styling

To pass all the linting checks you run the **black** and **mypy** commands, the commands should run in the docker volume.

```bash

# To run the black command
black .

# To run the mypy command
mypy .
```

> **Note:** The black command will change the code, so you need to run the command before committing the code. Also, the black can be configured so the files are formatted on save.


### 🧪 Testing

This code should have 100% of coverage, so before committing the code you need to run the tests and check the coverage. 
To know the coverage in the project you need to run the following command:

```bash

# To know the current coverage of the project. This command should be run in the docker volume
coverage run --source="./app" manage.py test && coverage html

# To open the html file with the coverage. This command should run in the normal command line inside of this folder
open htmlcov/index.html
```

To run the tests, if you are using pycharm, with the files saved in the `.run` folder, you can run the tests by using the pycharm interface.

## 📝 Documentation for development 

### 🗂️ Project structure

#### App structure

- **Domain** [`app/<component_name>/domain`]: This folder contains all the business logic of the project, and it's divided in the following folders:
    - `app/<component_name>/domain/exceptions.py`: This file contains all the exceptions that can have this component.
    - `app/<component_name>/domain/repositories.py`: This file contains the abstract repositories of the component. This will be implemented in the infrastructure folder.
    - `app/<component_name>/domain/models`: This folder contains all the models of the component.
    - `app/<component_name>/domain/usecases`: This folder contains all the use cases of the component.
  
- **Infrastructure** [`app/<component_name>/infrastructure`]: This folder contains all the infrastructure logic of the project, and it's divided in the following folders:
    - `app/<component_name>/infrastructure/persistance`: This folder contains all the logic related to the database.
        - `app/<component_name>/infrastructure/persistance/models`: This folder contains all the models of the component.
        - `app/<component_name>/infrastructure/persistance/<repository_file>`: This file is implementing the repository defined in the domain folder to apply the implementation to the database.
    - `app/<component_name>/infrastructure/http`: This folder contains all the files that applies to the http.
      - `app/<component_name>/infrastructure/views.py`: This file contains all the views of the component.
      - `app/<component_name>/infrastructure/urls.py`: This file contains all the urls of the component.
    - `app/<component_name>/infrastructure/repository_factories.py`: This file contains all the starting of the repository for the component.

- **Application** [`app/<component_name>/application`]: This folder contains all the application logic of the project, and it will have the following files:
  - `app/<component_name>/application/requests.py`: This file is implementing the different requests that can have the endpoints.
  - `app/<component_name>/application/responses.py`: This file is implementing the different responses that can have the endpoints.

#### Tests structure

- **Domain** [`tests/<component_name>/domain`]: This folder contains all the tests related to the domain of the component. The tests are divided in the following folders:
    - `tests/<component_name>/domain/usecases`: This folder contains all the tests related to the use cases of the component.
    - `tests/<component_name>/domain/<factory_file>`: This file the factory for any model so when creating it we can use it.

- **Infrastructure** [`tests/<component_name>/infrastructure`]: This folder contains all the tests related to the infrastructure of the component.
    - `tests/<component_name>/infrastructure/http`: This folder contains all the tests related to the http of the component. Inside, the views will be tested, the urls are testing indirectly.
    - `tests/<component_name>/infrastructure/persistence`: This folder contains all the tests related to the persistence of the component. Inside, the repositories will be tested, the models are testing indirectly.
    - `tests/<component_name>/infrastructure/test_repository_factories.py`: This file test the repository factories of the component.

- **Mocks** [`tests/<component_name>/mocks`]: This folder contains all the mocks implemented so the tests can run without making any change in production. The important mock is for the repository created for the database.

### 💡 Tips for development

#### Creating a new endpoint

To create a new endpoint you need to follow the following steps, there is an example in this [PR - For the base user creation](https://github.com/carlotacb/TFM-EventOrganizator/pull/9):

1. If the endpoint is the first endpoint created for a component we should do more steps:
   1. Create the structure of the component in the `app` folder, with the base files empty: `domain`, `infrastructure`, `application`.
      1. Create the `domain` folder with the following files: `exceptions.py`, `repositories.py`, `models`, `usecases`.
      2. Create the `infrastructure` folder with the following files: `persistance`, `http`, `repository_factories.py`.
      3. Create the `application` folder with the following files: `requests.py`, `responses.py`.
   2. Create the structure of the tests of the component in the `tests` folder. Following the same structure as the `app` folder.
   3. Create the ORM file inside the folder `app/<component_name>/infrastructure/persistance/models`.
      1. Important also to add the models in the `app/models.py`, before creating the migration, so it can be created correctly.
   4. After creating the ORM file, we need to run the following command in the docker volume:
      ```bash
      ./manage.py makemigrations
      ```
   5. Follow the steps of the base endpoint creation.

To create a new endpoint in a structure that already exists, there is an example in this [PR - User endpoint for get all](https://github.com/carlotacb/TFM-EventOrganizator/pull/10):

1. Create implementation for the repository (database and mock).
2. Implement use case for the implementation of that endpoint.
3. Implement the view for the endpoint.
   1. Important to add the url also in the files of the urls of the project `organizator_api/urls.py`.

---

## Useful commands

When there are changes in the database by anyone:
```bash 
# To make migrations

./manage.py migrate
```