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

:+1: :+1: :+1: :+1:
