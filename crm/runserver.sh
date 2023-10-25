python manage.py collectstatic --no-input
python manage.py migrate
gunicorn --worker-tmp-dir /dev/shm djcrm.wsgi # design for digital ocean, basically you just want to call gunicorn here