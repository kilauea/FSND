# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

## User's permissions management

  To be able to manage the user's permissions granted by Auth0 I've created a new module users/m2m.py to talk with the Auth0 paltform using the required API. As well I've created an new administrador role, and two new permissions:
  * manage:baristas
  * manage:managers

  The managers role has the manage:baristas permission which allows to modify baristas permissions, and the administrators role has both permissions to allow to modify baristas and managers permissions. Baristas are not allowd to modifiy any permissions.

  In order to handle the user's permissions from the frontend I've added four new endpoints to the backendend:

### GET /managers
- General:
  - Returns a dictionary with all the abailable users that an administrator is allowed to handle and success value
- Sample: `curl http://127.0.0.1:5000/managers`
```json
{
  "users": [
    {
      "id": "role_id",
      "name": "Barista",
      "permissions": [
        {
          "name": "get:drinks-detail",
          "valid": true
        },
        {
          "name": "post:drinks",
          "valid": false
        },
        {
          "name": "patch:drinks",
          "valid": false
        },
        {
          "name": "delete:drinks",
          "valid": false
        }
      ]
    },
    {
      "id": "role_id",
      "name": "Manager",
      "permissions": [
        {
          "name": "get:drinks-detail",
          "valid": true
        },
        {
          "name": "post:drinks",
          "valid": true
        },
        {
          "name": "patch:drinks",
          "valid": true
        },
        {
          "name": "delete:drinks",
          "valid": true
        }
      ]
    }
  ], 
  "success": true
}
```

### GET /baristas
- General:
  - Returns a dictionary with all the abailable users that a manager is allowed to handle and success value
- Sample: `curl http://127.0.0.1:5000/baristas`
```json
{
  "users": [
    {
      "id": "role_id",
      "name": "Barista",
      "permissions": [
        {
          "name": "get:drinks-detail",
          "valid": true
        },
        {
          "name": "post:drinks",
          "valid": false
        },
        {
          "name": "patch:drinks",
          "valid": false
        },
        {
          "name": "delete:drinks",
          "valid": false
        }
      ]
    }
  ], 
  "success": true
}
```

### PATCH /managers/<role_id>

- General:
  - Allows an administrador to modify the permissions for baristas and managers roles for the given role_id if exists. Returns the modified role_id and success value
- Sample: `curl http://127.0.0.1:5000/managers/rol_rBT608DLpQcBVKSf -X PATCH -H "Content-Type: application/json" -d '{"permissions":[{"name": "get:drinks-detail", "valid": true}, {"name": "post:drinks", "valid": false}, {"name": "patch:drinks", "valid": false}, {"name": "delete:drinks", "valid": false}]}'`
```json
{
  "role_id": "rol_rBT608DLpQcBVKSf",
  "success": true
}
```

### PATCH /baristas/<role_id>
- General:
  - Allows an administrador or manager to modify the permissions for baristas role for the given role_id if exists. Returns the modified role_id and success value
- Sample: `curl http://127.0.0.1:5000/baristas/rol_rBT608DLpQcBVKSf -X PATCH -H "Content-Type: application/json" -d '{"permissions":[{"name": "get:drinks-detail", "valid": true}, {"name": "post:drinks", "valid": false}, {"name": "patch:drinks", "valid": false}, {"name": "delete:drinks", "valid": false}]}'`
```json
{
  "role_id": "rol_rBT608DLpQcBVKSf",
  "success": true
}
```

### Heroku deployment

In order to be able to deploy the backend to Heroku I made several chages:
* Add a Procfile file with the commands to run the backend in Heroku: web: gunicorn --pythonpath src api:app. Thr option "--pythonpath src" is needed to avoid errors importing backend python modules
* Remove the local import paths from api.py
* Add a runtime.txt file to especify the Python version needed in Heroku
* The shell script herokuDeployment.sh contains the required commands to deploy the backend Git repository to Heroku

The backend app can be found at: [https://coffeeshop-backend.herokuapp.com](https://coffeeshop-backend.herokuapp.com)
