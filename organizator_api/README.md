# Organizator API

> API developed with Django

## How to start the project


## Development

### Creating a new model

Create a new model in the folder `app/<component_name>/infrastructure/persistance/models` and also add the import in the `app/models.py`. And then run the following command in the docker volume:

```bash 

./manage.py makemigrations
```

## Useful commands

``` bash
# To know the current coverage of the project

DJANGO_SETTINGS_MODULE=organizator_api.settings coverage run --source="./app" manage.py test && coverage html
```

When there are changes in the database by anyone:
```bash 
# To make migrations

./manage.py migrate
```