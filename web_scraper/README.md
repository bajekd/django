<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


![](gifs/1.gif)

## Getting Started

### Installation and run server on local machine
Prerequisites:
 * Python 3.9
 * Pipenv
 * redis
 * driver for your browser (selenium)

1. Clone repo
   ```
   cd ~/to/folder/where/you/want/clone/this/repo
   git clone https://github.com/blazejdobek/_django_web_scraper.git
   ```
2. Setting up project environment (require pipenv and redis)
   ```
   pipenv shell
   pipenv install
   ```
   * `xattr -d com.apple.quarantine <file_name>` --> allow to run your drivers for web browser (selenium) on macOS
   * `celery -A core worker -l info` --> run worker, connect to redis on port 6379 (settings.CELERY_BROKER_URL)
   * `celery -A core beat -l info` --> run scheduler (beat in your case - settings.CELERY_BEAT_SCHEDULE)

3. Enjoy!
   ```
   python manage.py runserver
   ```
## License

Distributed under the MIT License. See `LICENSE` for more information.

----
* `flower -A core --port=5555` --> require `pipenv install flower` (but it is incompatible with newest celery)

Future development ideas:
  * companies list generator project. --> add already seen to db, add scraping from https://justjoin.it/ // https://devresourc.es/jobs/remote-only // https://twitter.com/denicmarko/status/1304274720246738945 // https://it-leaders.pl/en
  * add [tags](https://django-tagging.readthedocs.io/en/develop/)
  * [deploy to aws](https://www.youtube.com/playlist?list=PLOLrQ9Pn6caz-6WpcBYxV84g9gwptoN20)
  * [build a dynamic filter form](https://www.youtube.com/playlist?list=PLLRM7ROnmA9EGO3TOlWLgrc46EhTgj1Ih)


redis-server // redis-cli // redis-cli shutdown