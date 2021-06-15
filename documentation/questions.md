# This private document

## Question 1

When we create in package file for example smoke.py and want 
to address this file as module in __init__.py of module Why we should write
`from .smoke import Smoke`  

## Question 2
Where I should import models first approach I made import in sales/__init__.py but I think it is not good.

## Question 3
Working with orders:
want to show name of worker instead of id for that additional study of context needed


## Question 4
in test_api_food.py test_post_food_wrong  if environment variable export FLASK_ENV=development is set we get Failture
```
AssertionError: b'{"message": "Wrong data"}\n' != b'{\n    "message": "Wrong data"\n}\n'
```
if this variable does not exist this test pass. 

I should study behavior where in test environment I must to set configuration.

## curl 
creation of food
```
curl -X POST http://localhost:5000/api/foods -d '{"name": "Simple cake", "price":3450 }' -H 'Content-Type: application/json'
``` 
