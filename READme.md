# Building a Messaging System with RabbitMQ, Celery and Python Application behind NGINX 

In the project We'll build a messaging system using Python Flask, Celery and RabbitMQ with NGINX

## Installation 

```````
// Install Python

$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
$ python3 -m venv myproject_env
$ source myproject_env/bin/activate

// Install Flask, Celery and RabbitMQ

$ pip install Flask celery
$ brew install rabbitmq


```````


``````
$ brew services start rabbitmq

``````
Checkout http://localhost:15672/
Login to RabbitMQ Management Interface using the following credentials:
- username: guest
- password: guest


```````
$ celery -A app.celery worker --loglevel=info
```````


``````
$ python app.py

``````

Now that Flask app should be running, and Celery should be able to process tasks. To test endpoints:

- For the `sendmail` parameter: Open a web browser and go to:  http://127.0.0.1:5000/?sendmail=test@example.com

- For the `talktome` parameter: Open the browser and go to: http://127.0.0.1:5000/?talktome

- After testing on the web, check the `~/messaging_system.log` on your root folder

````
$ ls ~/messaging_system.log
$ nano ~/messaging_system.log
````


