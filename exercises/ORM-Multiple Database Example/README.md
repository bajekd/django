[docs](https://docs.djangoproject.com/en/3.2/topics/db/multi-db/)
[Django Multiple Database Setup ](https://www.youtube.com/watch?v=g-FCzzzjBWo&list=PLOLrQ9Pn6cazjoDEnwzcdWWf4SNS0QZml&index=12)

admin // admin

add to your manage.py commands --database=<db_name>, except makemigration 
i.e:
python manage.py createsupersuer --database=users.db (<db_name> --> settings.DATABASES.key_name)


[Introduction to migrations and the Django database](https://www.youtube.com/watch?v=N4gjiJumTZg&list=WL&index=10)
[Django Dumpdata - Commands, Common Problem and how to overcome it](https://www.youtube.com/watch?v=CmWhiLclPHM&list=WL&index=11), [dumpdata - django docs](https://docs.djangoproject.com/en/3.2/ref/django-admin/#dumpdata)


python manage.py makemigrations
python manage.py migrate
python manage.py startapp blog
python manage.py sqlmigrate blog 0001
python manage.py showmigrations


to unapply migration:
python manage.py migrate <app_name> <migration_number> (i.e: 001)
python manage.py migrate <app_name> <migration_number> --plan (show which migrations will be unapply in order to unapply specify migration)


* `python manage.py dumpdata --indent 4 > <file_name>`(--database flag is required in this example, because we have here more than one db + we don't have default one)
* `python manage.py dumpdata <app_name> > <file_name>.json`  // `python manage.py dumpdata <app_name>.<table_name> > <file_name>.json`
* `python manage.py dumpdata --exclude <app_name>.<table_name> --indent 4 > <file_name>.json`

```
pip install pyaml
python manage.py dumpdata --indent 2 --format yaml > <file_name>.yaml
```

* `python manage.py flush` # clear all data from db, but do not remove applied migrations
* `python manage.py loaddata <file_name>` # problem with saving and recreating forein keys (auto generating id, then remove some of them, so you have entities id=1, 2, 3, 7, 10 ==> in new db when recreating them autogenerating will make it 1,2,3,4,5, so 10 doesn't exist and we have a problem ;))

* `python manage.py dumpdata --natural-foreign --natural-primary -e conttypes -e auth.Permission --indent 4 > db.json` (-e => exclude conttypes, because django can recreate it anyway)
