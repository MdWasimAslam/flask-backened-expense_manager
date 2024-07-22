import mysql.connector as mysql
import json
import jwt
from datetime import datetime,timedelta
from flask import make_response,jsonify

class user_model:
    
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
            
            
            
    
    def user_getall_model(self):
        self.cursor.execute('SELECT * FROM users')
        result = self.cursor.fetchall()
        print(result)
        if len(result) > 0:
            return result
        else:
            return 'No users found'
        

    def user_addOne_model(self,data):
        try:
                    self.cursor.execute('INSERT INTO users (name, email, phone, role, password ) VALUES (%s, %s, %s, %s,%s)', (data['name'], data['email'], data['phone'], data['role'], data['password']))
                    self.con.commit()
                    return 'User added successfully'
        except Exception as e:
                    return 'Error: ' + str(e)        
                
    def user_updateOne_model(self,data):
        try:
                    self.cursor.execute('UPDATE users SET name = %s, email = %s, phone = %s, role = %s, password = %s WHERE id = %s', (data['name'], data['email'], data['phone'], data['role'], data['password'], data['id']))
                    self.con.commit()
                    if self.cursor.rowcount > 0:
                        return 'User updated successfully'
                    else:
                        return 'Nothing to update'
        except Exception as e:
                    return 'Error: ' + str(e)  
                
    def user_deleteOne_model(self,data):
        try:
                    self.cursor.execute('DELETE FROM users WHERE id = %s', (data['id'],))
                    self.con.commit()
                    if self.cursor.rowcount > 0:
                        return 'User deleted successfully'
                    else:
                        return 'Nothing to delete'
        except Exception as e:
                    return 'Error: ' + str(e)  
                
                
    def user_getOne_model(self, id):
         try:
                    self.cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
                    result = self.cursor.fetchall()
                    if self.cursor.rowcount > 0:
                        return {"result":result},200
                    else:
                        return 'No user found'
         except Exception as e:
                    return 'Error: ' + str(e)
                
    
    def user_advUpdateOne_model(self,data,id):
        try:
                    query = 'UPDATE users SET '
                    for key in data:
                        query += key + ' = %s, '
                    query = query[:-2] + ' WHERE id = %s'
                    
                    self.cursor.execute(query, tuple(data.values()) + (id,))
                    self.con.commit()
                    if self.cursor.rowcount > 0:
                        return 'User updated successfully'
                    else:
                        return 'Nothing to update'
        except Exception as e:
                    return 'Error: ' + str(e)  
                
                
    def user_login_model(self, data):
        try:
            # Execute SQL query to fetch user details by matching email and password
            self.cursor.execute('SELECT id, name, email, phone, role_id FROM users WHERE email = %s AND password = %s', (data['email'], data['password']))
            
            # Fetch all results from the executed query
            result = self.cursor.fetchall()
            
            # Print the fetched results (for debugging purposes)
            print(result)
            
            # Get the first result (user details)
            userData = result[0]
            
            # Calculate expiration time for the token (current time + 5 minutes)
            exp_time = datetime.now() + timedelta(minutes=25)
            
            # Convert the expiration time to epoch format (seconds since Jan 1, 1970)
            exp_epoch = int(exp_time.timestamp())
            
            # Create the payload for the JWT token
            payload = {
                "payload": userData,
                'exp': exp_epoch
            }
            
            # Encode the payload to create a JWT token using the secret key 'secret' and HS256 algorithm
            jwtToken = jwt.encode(payload, 'secret', algorithm='HS256')
            
            # Check if any rows were affected (user exists)
            if self.cursor.rowcount > 0:
                # Return the JWT token in a response with status code 200 (OK)
                return make_response({'token': jwtToken}, 200)
            else:
                # Return 'Invalid credentials' if no matching user is found
                return 'Invalid credentials'
        
        except Exception as e:
            # Return the error message if any exception occurs
            return 'Error: ' + str(e)
