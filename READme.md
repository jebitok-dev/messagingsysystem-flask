# Building a Messaging System

In the project we'll build a messaging system that . The project requires one to use their email for testing and also create a password on App Console under Security settings this helps with Two-Factor Auth to keep your email safe and easily recover account incase of third party 

## Technologies 
- Python
- RabbitMQ
- Celery
- Nginx
- Ngrok

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
$ brew services restart rabbitmq
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

## NGINX 
`````
$ brew install nginx
// setup the nginx.config file 
`````
````
server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
`````

`````
$ sudo nginx -t
$ sudo nginx
`````

## NGROK 
- Create account on [NGROK website](https://dashboard.ngrok.com/get-started/setup/)


```````
$ brew install ngrok/ngrok/ngrok
$ ngrok config add-authtoken <replace_your_authtoken_here>
// deploy your app online 
$ ngrok http http://localhost:8080
// https://9906-102-215-34-198.ngrok-free.app -> http://localhost:8080 
```````

## Testing Project
- Make sure that NGINX is started or restarted and NGROK is running successfully under the port 80 like the one on the `nginx.config` file. You will see a line like this one:

`````
Forwarding                    https://6922-102-215-34-198.ngrok-free.app -> http://localhost:8080                                                                                             ``````
this shows the url which will replace the localhost
- Restart RabbitMQ `brew services restart rabbitmq`
- Run the Celery script `$ celery -A app.celery worker --loglevel=info`
- Run the python file `python app.py`
- Open [RabbitMQ dashboard](http://localhost:15672/) is open on the browser
Once this is done you will test the messaging system on the following link, on refresh the system will be sending a new email. 
https://6922-102-215-34-198.ngrok-free.app/?sendmail=test@example.com
https://6922-102-215-34-198.ngrok-free.app/?talktome

- You will check the output on your email 
- finally open the `~/messaging_system.log` file which is on your root folder of your system. You will see all logs of the system 
`````
$ nano ~/messaging_system.log
````` 

## Acknowledgement
I acknowledge [HNG Internship](https://hng.tech/internship) and our mentors for the DevOps Challenges and the support.