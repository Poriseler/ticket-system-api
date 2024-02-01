# Welcome to ticket-system-api 👋

> This is demo version of API for basic ticket system. Designed in mind to work in conjuction with dedicated front from my other repository as a portfolio project but this is not a limitation.

## Possible actions

#### For everyone

- View list of all tickets
- View details of a ticket
- Searching for ticket by ticket ID or ticket name
- View statictics regarding avarage closing ticket time, breakdown of all tickets by category and number of all tickets

#### For logged on users

- Creating a ticket
- Commenting on ticket
- Changing status of a ticket (owner and admin only)
- Displaying only tickets created by user
- Displaying only tickets assigned to user
- Displaying details of users profile
- Changing password
- Changing profile data
- Retrieving list of all employees

## Install

After downloading repository, only requirement is to install all dependecies from requirement.txt file. Use of virtual envirnment is encouraged but not obligatory.

```bash
# Clone the repository
git clone https://github.com/Poriseler/ticket-system-api.git

# Navigate to the project directory
cd ticket-system-api

# Optional virtual environement within env folder
python -m venv env

#Install dependencies
pip install -r requirements.txt
```

By default, CORS headers are allowed only from port `5173`. It may be extended or changed by adding an entry in `CORS_ALLOWED_ORIGINS` in `settings.py` file.

## Usage

By default frontend part of project expects backend to be on `8080` port, but it may be adapted to specific requirements or use with different APIs.

```python
py manage.py runserver 8080
```

## Used libraries

- [Django REST](https://www.django-rest-framework.org/)
- [corsheaders](https://pypi.org/project/django-cors-headers/)
- [drf_spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html)
- [djnago-rest-authtoken](https://pypi.org/project/django-rest-authtoken/)

## Swagger

Displaying interactive documentation of all endpoints along with parameters is possible thanks to Swagger. After starting an application it's availabe under `/api/docs/` address.
##Tests
Tests are split for each application within project but they can be run altogheter executing command

```python
py manage.py test
```

## Project status

Completed, although more functionalities may appear in future.
