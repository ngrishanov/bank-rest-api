# Bank REST API
Simple bank REST API.

API routes
----------

#### POST /accounts
Create an account.

**Request**

```
{
    "num": 1,  // integer > 0
    "amount": 1000 // integer >= 0
}
```

**Response**

```
{
    "success": true
}
``` 

#### GET /accounts/[num]
Get an account with `num` provided.

**Response**

```
{
    "success": true,
    "result": {
        "num": 1,
        "amount": 1000
    }
}
``` 

#### POST /transfer
Transfer amount from one account to another.

**Request**

```
{
    "num_from": 1,
    "num_to": 2,
    "amount": 500
}
```

**Response**

```
{
    "success": true,
    "result": {
        "amount_to": 500,
        "amount_from": 500
    }
}
``` 

How to run
----------
1. Make sure docker-compose is installed
2. Execute `prepare.sh`
3. Execute `docker-compose up -d` to run API

Libraries and tools used in project
-----------------------------------
- sanic (web server)
- asyncpg (PostgreSQL asyncio driver)
- PostgreSQL
- Docker and Docker-compose
