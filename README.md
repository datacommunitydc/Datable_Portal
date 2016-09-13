# Datable_Portal

#### Backend Setup Guide
* Install virtualenvwrapper
```sh
$ pip install virtualenvwrapper
```
First, some initialization steps. Most of this only needs to be done one time. 
You will want to add the command to `source /usr/local/bin/virtualenvwrapper.sh` 
to your shell startup file, changing the path to virtualenvwrapper.sh 
depending on where it was installed by pip.

* source 
```sh 
$ source /usr/local/bin/virtualenvwrapper.sh
```

* make ims virtual env
```sh
$ mkvirtualenv datable
```

* clone the repo
```sh
$ git clone https://github.com/GeneralInfluence/IMS.git
```
* go to backend folder
```sh
$ cd Datable_Portal/backend
```
* install requirements.txt
```sh
pip install -r requirements.txt
```
* sync database 
```sh
$ python manage.py migrate
```

* start backend server
```sh
$ python manage.py runserver
```



* Access the backend at 
```sh
http://localhost:8000
```


* Access the login with the url
```sh 
http://localhost:8000/accounts/login/
```

#### Frontend Setup Guide

* go to frontend folder
```sh
$ cd Datable_Portal/frontend
```

* install node packages
```sh
$ npm install
$ npm install --python=python2.7
```
* start frontend server
```sh
$ npm start
```

* Access the frontend at 
```sh
http://localhost:3000
```

#### Nginx Setup Guide

* open nginx default file
```sh
$ sudo vi /etc/nginx/sites-available/default
```
* add our application server config
```sh
server {
   listen 3000 default_server;

   root /.../frontend;
   index index.html index.htm;

   # Make site accessible from http://localhost/
   server_name localhost;

   location / {
      try_files $uri /index.html;
   }

   location /datable_backend_app/ {
      proxy_pass http://localhost:8000/;
   }

  location /linkedin/ {
      proxy_pass https://www.linkedin.com/;
  }

  location /twitter/ {
      proxy_pass https://api.twitter.com/;
  }
  
  location /meetup/ {
      proxy_pass https://secure.meetup.com/;
  }
  
  location /github/ {
      proxy_pass https://github.com/;
  }
}

```

* restart the nginx service
```sh
  $ sudo service nginx restart
```

* Access the frontend at 
```sh
  http://127.0.0.1:3000/
  
  Please don't use localhost as some of the social login provider (like twitter, meetup etc.) don't support localhost for redirect_uri.
```

:+1: :+1: :+1: :+1:
