Steps to setup and run

IN CMD IN A NEW FOLDER

> git clone https://github.com/faridstage/DjangoTask

> cd DjangoTask

> code .

> IT WILL OPEN THE PROJECT IN VSCODE

OPEN DOCKER DESKTOP ON YOUR MACHINE

OPEN TERMINAL IN VSCODE AND RUN

> docker-compose build db

> docker-compose up db // this will run only db container first

OPEN ANOTHER TERMINAL AND RUN

> docker-compose build web --no-cache

> docker-compose up web --build

OPEN THIRD TERMINAL AND SEED THE DUMMY DATA

> docker-compose exec web python seed.py

OPEN ANY BROWSER AND TYPE
http://127.0.0.1:8000/admin

LOGIN AS ADMIN(farid)
username => farid
password => Farid@1234

THEN IN A NEW TAP IN BROWSER TYPE
http://127.0.0.1:8000/orders (this is the home page)

##ENJOY ;)
