# Django Rest Example
This is a simple example of a Django Rest API.

## Installation
1. Clone the repository
2. type `pip install -r requirements.txt` to install the dependencies
<br>

`Note: Database already created, no need to create a new one`

## Usage
type `python3 run.py` to start the server 


## Paths

### Public
### `/api/register` - POST - Register a new user
### `/api/login` - POST - Login a user
   
### Authenticated
JWT Token is required for all the following paths set to HTTP Header `Authorization: Bearer {token}`

**Admin Account Test:**
```
email: admin@admin.com
password: admin
```

### `/api/admin/users` - GET - Get all users
### `/api/admin/create-user` - POST - Create a new user
Example of the body:
```json
{   
    "name": "Full Name",
    "email": "user@mail.com",
    "password": "password",
    "is_admin": false
}
```
### `/api/admin/users/id/{id}` - GET - Get a specific user
### `/api/admin/users/id/{id}` - PUT - Update a specific user
Example of the body:
```json
{   
    "name": "Full Name",
    "email": "user@mail.com",
    "password": "password",
    "is_admin": false
}
```
### `/api/admin/users/id/{id}` - DELETE - Delete a specific user

