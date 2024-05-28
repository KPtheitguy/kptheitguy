
 _  ______    _____ _   _ _____   ___ _____    ____ _   ___   __
| |/ /  _ \  |_   _| | | | ____| |_ _|_   _|  / ___| | | \ \ / /
| ' /| |_) |   | | | |_| |  _|    | |  | |   | |  _| | | |\ V / 
| . \|  __/    | | |  _  | |___   | |  | |   | |_| | |_| | | |  
|_|\_\_|       |_| |_| |_|_____| |___| |_|    \____|\___/  |_|  
                                                                



################################################################################################
#   MIT License                                                                                #
#                                                                                              #
#    Copyright (c) [2024] [Koushik Polsana]                                                    #
#                                                                                              #
#    Permission is hereby granted, free of charge, to any person obtaining a copy              #
#    of this software and associated documentation files (the "Software"), to deal             #
#    in the Software without restriction, including without limitation the rights              #
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell                 #
#    copies of the Software, and to permit persons to whom the Software is                     #
#    furnished to do so, subject to the following conditions:                                  #
#                                                                                              #
#    The above copyright notice and this permission notice shall be included in all            #
#    copies or substantial portions of the Software.                                           #
#                                                                                              #
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR                #
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,                  #
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE               #
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER                    #
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,             #
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE             #
#    SOFTWARE.                                                                                 #
#                                                                                              #
################################################################################################


FastAPI Authentication and User Creation

This FastAPI application provides endpoints for user authentication and user creation. It uses MongoDB as the database to store user information.

Table of Contents

Installation
Configuration
Running the Application
API Endpoints
Authenticate User
Create User
Usage
Installation

Clone the repository:

sh
Copy code
git clone https://github.com/KPtheitguy/kptheitguy.git
cd your-repository
Create and activate a virtual environment:

sh
Copy code
python3 -m venv fastapidb



source fastapidb/bin/activate
Install the required packages:

sh
Copy code
pip install -r requirements.txt
Configuration

Update inputs.json with your database credentials:
json
Copy code
{
    "active_db": "mongodb",
    "mongodb": {
        "uri": "",
        "database_name": "",
        "collection_name": ""
    },
    "jwt_secret_key": "your_secret_key",
    "jwt_algorithm": "HS256",
    "token_expiry_hours": 24
}
Running the Application

Start the FastAPI application:

sh
Copy code
uvicorn app.main:app --reload
Access the API documentation:
Open your web browser and navigate to http://127.0.0.1:8000/docs to see the Swagger UI.

API Endpoints

Authenticate User
Endpoint: /auth/token

Method: POST

Description: Authenticates a user and returns a JWT token.

Request Body:

json
Copy code
{
    "username": "string",
    "password": "string"
}
Response:

json
Copy code
{
    "access_token": "string",
    "token_type": "bearer"
}
Create User
Endpoint: /users/create

Method: POST

Description: Creates a new user. Requires a valid JWT token in the request body.

Request Body:

json
Copy code
{
    "first_name": "string",
    "last_name": "string",
    "username": "string",
    "password": "string",
    "email": "string",
    "phone_number": "string",
    "token": "string"
}
Response:

json
Copy code
{
    "message": "User created successfully"
}
Usage

Authenticate User
Send a POST request to /auth/token with the username and password:

sh
Copy code
curl -X POST "http://127.0.0.1:8000/auth/token" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
    "username": "johndoe",
    "password": "password123"
}'
Get the JWT token from the response:

json
Copy code
{
    "access_token": "your_jwt_token",
    "token_type": "bearer"
}
Create User
Send a POST request to /users/create with the new user details and the JWT token:

sh
Copy code
curl -X POST "http://127.0.0.1:8000/users/create" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "password": "password123",
    "email": "johndoe@example.com",
    "phone_number": "1234567890",
    "token": "your_jwt_token"
}'
Get the success message from the response:

json
Copy code
{
    "message": "User created successfully"
}
