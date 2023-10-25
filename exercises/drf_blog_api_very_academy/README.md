python manage.py makemigrations --dry-run --verbosity 3

## permissions problem
if in your permission table in db there aren't any data, do this:
1. install [Django Extensions](https://github.com/django-extensions/django-extensions)
2. Run `python manage.py update_permissions`