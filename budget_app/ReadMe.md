
![](gifs/1.gif)

![](gifs/2.gif)

![](gifs/3.gif)

## Getting Started


### Installation and run server on local machine
Prerequisites:
 * Python 3.9
 * Pipenv
 * postgresql
 
### Install project env:
1. Clone repo 
   ```
   cd ~/to/folder/where/you/want/clone/this/repo
   git clone https://github.com/blazejdobek/_django_e_commerce.git
   ```
2. Setting up project environment (require pipenv)
   ```
   pipenv shell
   pipenv install
   ```
3. Create postgreSQL db:

    ```
    createdb DB_NAME // psql -l #list available databases
    psql DB_NAME
    CREATE USER user_name WITH PASSWORD 'top_secret_password';
    GRANT ALL PRIVILEGES ON DATABASE db_name TO user_name;
    \q
    ```
4. Create `.env` file
  * Create a new file named .env inside the budget_app folder (`budget_app/.env`)
  * Copy all of the variables from `budget_app/.template.env` and assign your own values to them

    ```
    mv budget_app/.env.template .env
    # ASSIGN YOUR OWN VALUES TO .ENV file (db and email credentials)
    ```
5. Run server 
    ```
    export READ_DOT_ENV_FILE=True
    python manage.py runserver
    ```
    </br>
Users:
* to register new user: `http://127.0.0.1:8000/authentication/register/`
   
6. Testing
  * in order to run selenium test:
      * Download, and install [chrome](https://www.google.com/chrome/)
      * `brew instal --cask chromedriver` (you may need add driver path to PATH)
    
  ```
  python manage.py test # run all tests
  coverage run  manage.py test && coverage report && coverage html # run all test, print report to cli and create html report 
  coverage run -m pytest && coverage report # coverage report
  coverage run --source=authentication/ manage.py test` # run tests only for choosen app (in this example for authentication app)
  ```
  
### Troubleshooting
* in order to properl work with `from weasyprint import HTML` (on macOS; dependencies from `expenses/views.py`) i needed to install: 

  ```brew install cairo pango gdk-pixbuf libxml2 libxslt libffi```
  
### Ideas for improvement
  * user can add Categories (for expenses), likewise user can add sources (for income), creting both of them from csv file
  * create tree-structure from table Categories
  * in export to csv, exel and pdf --> how add ie. '.csv' to filename (without being PURGE!)


## Resources
* [project_playlist_1](https://www.youtube.com/playlist?list=PLx-q4INfd95G-wrEjKDAcTB1K-8n1sIiz)
* [project_playlist_2](https://www.youtube.com/playlist?list=PLx-q4INfd95H5uJKX0edqpbFHVXGrB1Pc)
* [http status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
* [django signals](https://www.youtube.com/watch?v=W8MLlwvSS-U)
* [django_testing_mozilla_developer](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing)
* [django_testing_real_python](https://realpython.com/testing-in-django-part-1-best-practices-and-examples/)
