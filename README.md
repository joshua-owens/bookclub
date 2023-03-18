### Local Development

Start up the containers
```shell
docker-compose up -d
```

Run migrations
```shell
docker-compose run web python manage.py migrate
```

Create a superuser
```shell
docker-compose run web python manage.py createsuperuser
```