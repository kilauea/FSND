import sys
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from .users.m2m import Auth0Manager

app = Flask(__name__)
setup_db(app)
CORS(app)
m2m = Auth0Manager()

def get_users(users):
  users_list = []
  scopes = []
  resource_server_name = 'Coffee Shop'
  coffee_shop_server_and_roles = m2m.getResourceServerAndRoles(resource_server_name)

  if len(coffee_shop_server_and_roles) > 0:
    for role in coffee_shop_server_and_roles['roles']:
      if role['name'] in users:
        permissions = m2m.getRolePermissions(role['id'], resource_server_name)
        if len(permissions) > 0:
          user_permissions = [permission['permission_name'] for permission in permissions]
          user_scopes = [{'name': scope['value'], 'valid': scope['value'] in user_permissions} for scope in coffee_shop_server_and_roles['resource_server']['scopes']]

          users_list.append({
            'id' : role['id'],
            'name': role['name'],
            'permissions': user_scopes
          })
  return users_list

'''
@implement endpoint
    GET /managers
        public endpoint
    returns status code 200 and json {"success": True, "users": users} where users is the list of users
        that can be managed with manage:managers permission, or appropriate status code indicating reason for failure
'''
@app.route('/managers')
@requires_auth('manage:managers')
def manage_managers(jwt):
  return jsonify({
    'success': True,
    'users': get_users(['Barista', 'Manager'])
  })

'''
@implement endpoint
    GET /baristas
        public endpoint
    returns status code 200 and json {"success": True, "users": users} where users is the list of users
        that can be managed with manage:baristas permission, or appropriate status code indicating reason for failure
'''
@app.route('/baristas')
@requires_auth('manage:baristas')
def manage_baristas(jwt):
  return jsonify({
    'success': True,
    'users': get_users(['Barista'])
  })

'''
@implement endpoint
    GET /managers/role_id
        public endpoint
    returns status code 200 and json {"success": True, "users": users} where users is the list of users
        or appropriate status code indicating reason for failure
'''
@app.route('/managers/<role_id>', methods=['PATCH'])
@requires_auth('manage:managers')
def patch_managers(jwt, role_id):
  body = request.get_json()
  role_id = body.get('id', None)
  new_permissions = body.get('permissions', None)
  if not role_id or not new_permissions:
      abort(422)
  m2m.patchRolePermissions(role_id, new_permissions, 'Coffee Shop')
  return jsonify({
    'success': True,
    'id': role_id
  })

'''
@implement endpoint
    GET /baristas/role_id
        public endpoint
    returns status code 200 and json {"success": True, "users": users} where users is the list of users
        or appropriate status code indicating reason for failure
'''
@app.route('/baristas/<role_id>', methods=['PATCH'])
@requires_auth('manage:baristas')
def patch_baristas(jwt, role_id):
  body = request.get_json()
  role_id = body.get('id', None)
  new_permissions = body.get('permissions', None)
  if not role_id or not new_permissions:
      abort(422)
  m2m.patchRolePermissions(role_id, new_permissions, 'Coffee Shop')
  return jsonify({
    'success': True,
    'id': role_id
  })

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
  drinks = Drink.query.all()
  ret = jsonify({
    'success': True,
    'drinks': [drink.short() for drink in drinks]
  })
  return ret

'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
  drinks = Drink.query.all()
  return jsonify({
      'success': True,
      'drinks': [drink.long() for drink in drinks]
    })


'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(jwt):
  body = request.get_json()
  try:
    # Create a new drink
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    if not title:
      abort(422)
    drink = Drink(title=title, recipe=json.dumps(recipe))
    drink.insert()

    return jsonify({
      'success': True,
      'drinks': [drink.long()]
    })
  except:
    print(sys.exc_info())
    abort(422)

'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drinks(jwt, drink_id):
  body = request.get_json()
  try:
    drink = Drink.query.get(drink_id)
    if drink is None:
      abort(404)
    # Edit the drink with id=drink_id
    title = body.get('title', None)
    if title != None:
      drink.title = title
    recipe = body.get('recipe', None)
    if recipe != None:
      drink.recipe = json.dumps(recipe)
    drink.update()

    return jsonify({
      'success': True,
      'drinks': [drink.long()]
    })
  except:
    print(sys.exc_info())
    abort(422)

'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, drink_id):
  try:
    drink = Drink.query.get(drink_id)
    if drink is None:
      abort(404)
    # Delete the drink with id=drink_id
    drink.delete()

    return jsonify({
      'success': True,
      'delete': drink_id
    })
  except:
    print(sys.exc_info())
    abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
    "success": False, 
    "error": 422,
    "message": "unprocessable"
  }), 422

'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@DONE implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
  return jsonify({
    "success": False, 
    "error": 404,
    "message": "resource not found"
    }), 404

'''
  Error handler for 400: bad request
'''
@app.errorhandler(400)
def bad_request(error):
  return jsonify({
    "success": False, 
    "error": 400,
    "message": "bad request"
    }), 400

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def handle_auth_error(error):
  return jsonify({
    "success": False, 
    "error": error.status_code,
    "message": error.error['description']
    }), error.status_code
