# Sales 2021

[![GitHub Stars](https://img.shields.io/github/stars/m7vv/sales2021.svg)](https://github.com/m7vv/sales2021/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/m7vv/sales2021.svg)](https://github.com/m7vv/sales2021/issues) [![Current Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/m7vv/sales2021)
[![Coverage Status](https://coveralls.io/repos/github/m7vv/sales2021/badge.svg)](https://coveralls.io/github/m7vv/sales2021)

Simple webservice for saving information about sales of food in snack bars.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Testing](#testing)

## General info
Educational project for Online Python External program

## Technologies
Project is created with:
* Python
* Flask
* VueJs

## Setup
To run this project, install it locally using pip
First run backend
For Linux or Mac
```bash
export FLASK_APP=sales
export FLASK_ENV=development
flask run
```
To run with gunicorn use for example command
```bash
gunicorn -b localhost:5000 -w 2 wsgi:app
```

To run web client (frontend)
```bash
cd client
npm run serve
```
then in browser open   http://localhost:8080/food 
## Testing
Using of unit test
```
python -m unittest discover
```
Using of coverage
```
coverage run -m unittest discover
coverage report
```
or for only for backend
```
coverage run --source=sales -m unittest discover

```