# Transaction API

API service for transactions management written on Django Rest Framework


### Installing using GitHub

- Python3 must be already installed
- Install PostgreSQL and create db


```shell
git clone https://github.com/Viktor-Beniukh/transaction-api-test-task.git
cd transaction-api-test-task
python3 -m venv venv
source venv/bin/activate (for Linux or macOS) or venv\Scripts\activate (for Windows)
pip install poetry
poetry install
python manage.py migrate
python manage.py runserver   
```

You need to create directory `static`

You need to create `.env.prod` file and add there the variables with your according values 
to run the project into docker (e.g. `.env.prod.sample`):
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;
- `DJANGO_DEBUG=False`;


To check functionality of the project without docker, you need to create `.env` file and add there the variables 
with your according values (e.g. `.env.sample`):
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;
- `DJANGO_DEBUG=True`;

Optional: you can add a variable called `LOG_LEVEL` to `.env` and `.env.prod` files, if you want to change a level of logging


## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up` or `docker-compose up -d` (to work in this terminal)



## Getting access

- Create admin via /api/user/register-admin/
- Get token authentication via /api/user/login-admin/
- Logout and delete token authentication via /api/user/logout-admin/


## Features

- Token authentication;
- Admin panel /admin/;
- Documentation is located at /api/v1/doc/swagger/;
- Creating, reading, updating and deleting users (only admin);
- Creating, reading, updating and deleting transactions (only admin);
- Filtering transactions by type transactions and date (only admin);


### How to create superuser
- Run `docker-compose up` command, and check with `docker ps`, that all services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there (web image);


### What do APIs do

- [GET] /api/v1/transactions/ - obtains a list of transactions with the possibility of filtering by type transactions and date (only admin);
- [GET] /api/v1/transactions/id/ - obtains the specific transaction information data (only admin);
- [POST] /api/v1/transactions/ - creates a transaction (only admin);
- [PUT] /api/v1/transactions/id/ - updates the transaction data (only admin);
- [PATCH] /api/v1/transactions/id/ - partial updates the transaction data (only admin);
- [DELETE] /api/v1/transactions/id/ - deletes the transaction data (only admin);

- [GET] /api/user/clients/ - obtains a list of users with transactions (only admin);
- [GET] /api/user/clients/id/ - obtains the specific user with transactions (only admin);
- [POST] /api/user/clients/ - creates a new user (only admin);
- [PUT] /api/user/clients/id/ - updates the user data (only admin);
- [PATCH] /api/user/clients/id/ - partial updates the user data (only admin);
- [DELETE] /api/ser/clients/id/ - deletes the user (only admin);

- [POST] /api/user/register-admin/ - creates new admin;
- [POST] /auth/user/login-admin/ - creates token authentication for admin;
- [POST] /auth/users/logout-admin/ - log out admin and delete token authentication;


### Checking the endpoints functionality
- You can see detailed APIs at swagger page: `http://127.0.0.1:8000/api/v1/doc/swagger/`.



## Check project functionality

Superuser credentials for test the functionality of this project:
- username: `UserMigrate`;
- password: `migratedpassword`.
