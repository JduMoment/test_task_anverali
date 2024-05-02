# Project Overview

Welcome to the Freelancer Website! This project showcases the basic functionality of a website for freelancers.

## Features

- **User Registration**: Create an account by filling in the registration form and saving the user to the database.
- **User Authentication**: Log in to your account using user memorization.
- **Different Profiles**: Switch between performer and customer profiles, each with different fields to fill in.
- **Profile Switching**: Switch between profiles without requiring re-authorization.
- **Log Out**: Log out of your account.
- **Admin Interface**: Access the admin interface for managing the website.

## Technologies Used

This project is built using the following technologies:

- Python 3.10
- Flask: A web framework for building web applications.
- SQLAlchemy 2.0: An Object-Relational Mapping (ORM) library for Python.
- Alembic: A database migration tool for SQLAlchemy.
- Flask-Login: A user session management extension for Flask.
- Flask-Admin: A simple and flexible admin interface framework for Flask.
- Psycopg2: A PostgreSQL database adapter for Python.


## Getting Started

You must first install docker-compose and poetry.

To test the web application locally, follow these steps:

1. Clone or extract project and open directory `test_task_anverali`.
2. Make a copy of the `.env.database.example` file and rename it to `.env.database`.
3. Make a copy of the `.env.example` file and rename it to `.env`.
4. Install all the dependencies using the `make install` command.
5. Edit the `DATABASE_URL` variable in the `.env` file with your PostgreSQL database credentials.
6. Run `sudo docker-compose build` in the terminal.
7. Run `sudo docker-compose up` in the terminal to start the application.
8. To stop the application, run `sudo docker-compose down`.
