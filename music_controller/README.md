<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

![](gifs/1.gif)


## Getting Started

1) To use the available functions, you must have a premium account at spotify (e.g. play/pause or skip API calls are allowed only for premium users).
2) Application indicates currently playing song on given host spotify account -> please remember to run some music on spotify to use all app functionalities.


### Installation and run server on local machine
Prerequisites:
 * Python 3.9
 * Pipenv
 * node.js

1. Clone repo
   ```
   cd ~/to/folder/where/you/want/clone/this/repo
   git clone https://github.com/blazejdobek/_drf_music_controller.git
   ```
2. Setting up project environment (require pipenv and node.js)
   ```
   pipenv shell
   pipenv install
   cd frontend/ && npm install
   ```
3. Before run server make sure to export READ_DOT_ENV_FILE=True. Enjoy!
   ```
   export READ_DOT_ENV_FILE=True
   python manage.py runserver
   ```
## License

Distributed under the MIT License. See `LICENSE` for more information.

----

Future development ideas:
* add auth with rest
* ability to have many rooms for host
* how to sygnalize to end user that in case of not having spotify premium you can't pause/play/skip song => status=200, but { {message="Forbidden"}}
* deploy on Amazon AWS.




