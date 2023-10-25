![](https://github.com/blazejdobek/_django_e_commerce/actions/workflows/python-package.yml/badge.svg)


<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#live-and-usage">Live and usage</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#what-have-i-learned">What have I learned</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

![](gifs/2.gif)


![](gifs/3.gif)

## Usage
 To make payment use this paypal sandbox account:
   * email: sb-y3gtj5957501@personal.example.com
   * passwd: X[?bb1$.


### Installation and run server on local machine
Prerequisites:
 * Python 3.9
 * Pipenv

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
3. Enjoy!
   ```
   python manage.py runserver
   ```
 4. Testing
   ```
   coverage run -m pytest && coverage report # coverage report
   pytest # run all tests
   pytest ecommerce/apps/catalogue/ # run tests only for catalogue app
   pytest ecommerce/apps/catalogue/tests/test_models.py -k test_category_generate_properly_slug # run only specify test (test_category_generate_properly_slug from catalogue app)
   ```

## What have I learned
* how and structurize slightly bigger project and most popular ways to do so
* using github action to imitate some of CI/CD proccess
* session, and how we can use them
* writing custom user model by extending AbstractBaseUser
* passing env vars, especially handle them with js without passing them explicite into js file (with making custom template filter)
* using django mptt (for product categories)
* solution to n+1 query problem + how to detect it with django-debug-toolbar
* making ajax call with jquery
* writing tests with pytest
* integration with paypal
* generate dummy date with faker and django commands
* the tedious art of debugging (with pdb)
* basic of deployment, potencial issues

## License

Distributed under the MIT License. See `LICENSE` for more information.


----
## Resources
* [base playlist](https://www.youtube.com/playlist?list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_)
* [pytest](https://www.youtube.com/playlist?list=PLOLrQ9Pn6caw3ilqDR8_qezp76QuEOlHY)
* [github actions](https://www.youtube.com/watch?v=qJPLFDtEi1I&list=WL&index=2)
* [deploy via heroku button](https://www.youtube.com/watch?v=AzAlfH2Vl2Q)
* [Faker](https://www.youtube.com/watch?v=8LHdbaV7Dvo&list=WL&index=1)

## Next:
* [generating more realistic fake data](https://www.youtube.com/watch?v=VJBY2eVtf7o&list=WL&index=5)
* [models best practice](https://sunscrapers.com/blog/6-expert-tips-for-building-better-django-models/)
* aws deployment
