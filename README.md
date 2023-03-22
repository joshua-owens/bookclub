### Local Development

Copy the `.env.example` and fill in the required variables

```shell
cp .env.example .env
```

Start up the containers
```shell
docker-compose up -d
```

Make Migrations

```shell
docker-compose run web python manage.py makemigrations
```

Run migrations
```shell
docker-compose run web python manage.py migrate
```

Create a superuser
```shell
docker-compose run web python manage.py createsuperuser
```

Collect Static Assets
```shell
docker-compose run web python manage.py collectstatic
```

Seed the discord credentials into the database for allauth

```shell
docker-compose run web python manage.py load_discord_social_app
```