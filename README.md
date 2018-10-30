[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/jonathanmusila/Store-Manager-V2/blob/master/LICENSE)

## Store Manager

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.


## Endpoints

| Endpoint       | Description          |   HTTP-verb  |
| ------------- |:-------------:| -----:| 
| /api/v1/products | Post a product | POST |
| /api/v1/sales  | Post a sale record      | POST   |
| /api/v1/products | Get all products |  GET |
| /api/v1/product/id | Get product by id | GET |
| /api/v1/sales | Get all sale records | GET |
| /api/v1/sales/id | Get a record by id | GET|
| /api/v1/products | Get all a product and update it |  PUT |
| /api/v1/products/id | Get product by id and delete it| DELETE |
| /api/v1/users/register | Post a user | POST |
| /api/v1/users/login | Post a login | POST|

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
A few requirements to install, run and test this project.

cd path/to/directory-your-directory
- git clone https://github.com/jonathanmusila/Store-Manager-V2.git
 -Install virtual environment 
- cd to Store-Manager-V2 and execute the following commands:
    
    - $ virtualenv -p python3 env 
    - $ source env/bin/activate
    - $ pip install -r requirements.txt
    - $ pip install pytest

- run the create table fucntion 

    - $ python3 migration.py
    
- To run tests, do:

    - $ pytests

- Then run the app by executing:
    - $ python3 run.py
    
- Install postman to test the various endpoints

## Testing
Manually, open the Postman and test all the endpoints.

## Built With
* python

## Authors
Jonathan Musila
