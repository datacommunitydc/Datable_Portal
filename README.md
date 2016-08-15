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
pip install -r requirement.txt
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

:+1: :+1: :+1: :+1:
