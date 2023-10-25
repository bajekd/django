### Install project env:

```
pipenv shell
pipenv install
```

### Create postgreSQL db:

```
createdb DB_NAME // psql -l #list available databases
psql DB_NAME
CREATE USER user_name WITH PASSWORD 'top_secret_password';
GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;
\q
```

### Before runserver:

* Create a new file named `.env` inside the djcrm folder
* Copy all of the variables inside `djcrm/.template.env` and assign your own values to them
```
export READ_DOT_ENV_FILE=True
python manage.py tailwind build
python manage.py collectstatic
npm run build # need to be in jstoolchain folder
python manage.py runserver
```
