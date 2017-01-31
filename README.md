# bucketlist-cp2
[![Build Status](https://travis-ci.org/andela-ian/bucketlist-cp2.svg?branch=master)](https://travis-ci.org/andela-ian/bucketlist-cp2)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/99171a3146c14de3be6410a8bcccafe5)](https://www.codacy.com/app/andela-ian/bucketlist-cp2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-ian/bucketlist-cp2&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/99171a3146c14de3be6410a8bcccafe5)](https://www.codacy.com/app/andela-ian/bucketlist-cp2?utm_source=github.com&utm_medium=referral&utm_content=andela-ian/bucketlist-cp2&utm_campaign=Badge_Coverage)
--------------------------------------------------
This is a bucketlist service API built using Flask.

Bucketlist API allows you to manage your own bucketlists.

Features include registering and authenticating a user;
creating, retrieving, updating and deleting bucketlist data and bucketlist item data.

###MIME Type
The MIME type for requests is always application/json


###EXAMPLE Requests
```
curl -i -H 'Accept: application/json' 'http://localhost:5000/register'

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 159
Server: Werkzeug/0.10.4 Python/3.5
Date: Fri, 27 Jan 2016 17:33:15 GMT

{"message": "Welcome to the bucketlist service", "more": "To register make a POST request to /register ENDPOINT with [username] and [password]"}
```

*NOTE THAT* upon login, the generated token must be specified in the subsequent request headers. An example of how this looks is:
```
Authorization: Bearer <token>
```

###First Things, First
You should do an install of all package requirements in your python setup or go about creating a virtual environment. 
```
pip install -r requirements.txt
```
###Create Database Tables
You need to initialize database and tables. The following command does this and also adds a new user 
with credentials: username _john_, password _oldman_
```
python manager.py createdb -t
```

###How To Start The Server
Run the following command to start the server and begin listening for requests to each endpoints.
```
python run.py development
```

You can get available environment options by running:
```
python run.py -h
```

###Available Endpoints

| Endpoint | Description |
| ---- | --------------- |
| [POST /auth/login](#) | Login user. Session token is valid for an hour|
| [POST /auth/logout](#) | Logout user. |
| [POST /auth/register](#) |  Register user. Request should have _username_ and _password_ in form data. |
| [POST /bucketlists/](#) | Create a new bucket list. Request should have _name_ in form data. |
| [GET /bucketlists/](#) | List all the created bucket lists. |
| [GET /bucketlists/:id](#) | Get single bucket list. |
| [PUT /bucketlists/:id](#) | Update single bucket list. Request should have _name_ in form data. |
| [DELETE /bucketlists/:id](#) | Delete single bucket list. |
| [POST /bucketlists/:id/items](#) | Add a new item to this bucket list. Request should have _name_, _done_(defaults to False) in form data. |
| [PUT /bucketlists/:id/items/:item_id](#) | Update this bucket list. Request should have _name_, _done_(True or False) in form data. |
| [DELETE /bucketlists/:id/items/:item_id](#) | Delete this single bucket list. |
| [GET /bucketlists?limit=20](#) | Get 20 bucket list records belonging to user. Allows for a maximum of 100 records. |
| [GET /bucketlists?q=bucket1](#) | Search for bucket lists with bucket1 in name. |



