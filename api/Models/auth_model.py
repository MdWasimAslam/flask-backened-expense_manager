import mysql.connector as mysql
import json
import jwt
import re
from datetime import datetime,timedelta
from flask import make_response,jsonify,request

class auth_model:
    
    def __init__(self):
       try:
            self.con = mysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'Wasim@slam1998',
            database = 'myDb'
            )
            print('Connected to the database')
            self.cursor = self.con.cursor(dictionary=True)
       except Exception as e:
            print('Error:', e)
       return None  
   
   
   
   
   #Decorator to check if the user has access to the api endpoint
    def token_auth(self,endpoint):
       def inner1(func):
           def inner2(*args):
               authorisation = request.headers.get('Authorization')
               if re.match("^Bearer *([^ ]+) *$",authorisation,flags=0):
                    token = authorisation.split(' ')[1]
                    jwtdecode = jwt.decode(token,'secret',algorithms=['HS256'])
                    role_id = jwtdecode['payload']['role_id']
                    self.cursor.execute('SELECT roles FROM accessibility_view WHERE endpoint = %s',(endpoint,))
                    result = self.cursor.fetchone()
                    if(len(result) > 0):
                        roles = json.loads(result['roles'])
                        if role_id in roles:
                            return func(*args)
                        else:
                            return {'message':'You do not have access to this endpoint!'},403
                    else:
                        return {'message':'Endpoint not found!'},404
               elif authorisation is None:
                  return {'message':'No Token Provided!'},401
               else:
                     return {'message':'Invalid Token!'},401
           return inner2
       return inner1