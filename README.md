# Coffee Shop - Flask Practice

For this assessment, you'll be working with a Coffee Shop domain.

In this repo:

- There is a Flask application with some features built out.

You can either check your API by:

- Using Postman to make requests
- Building out a React frontend

## Setup

To download the dependencies, run:

```console
pipenv install
pipenv shell
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

## Models

You will implement an API for the following data model:

![Coffee Shop ERD](./coffee-shop-erd.png)

The file `server/models.py` defines the model classes **without relationships**.
Use the following commands to create the initial database `app.db`:

```console
export FLASK_APP=server/app.py
flask db init
flask db upgrade head
```

Now you can implement the relationships as shown in the ER Diagram:

- A `Customer` has many `Coffee`s through `Order`
- A `Coffee` has many `Customer`s through `Order`
- A `Order` belongs to a `Customer` and belongs to a `Coffee`

Update `server/models.py` to establish the model relationships. Since a
`Order` belongs to a `Customer` and a `Coffee`, configure the model
to cascade deletes.

Set serialization rules to limit the recursion depth.

Run the migrations and seed the database:

```console
flask db revision --autogenerate -m 'message'
or 
flask db migrate -m 'message'
flask db upgrade head
python server/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.

## Validations

Add validations to the `Order` model:

- must have a `price` greater than or equal to 2

Add validations to the `Coffee` model:

- must have a unique `name`

## Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using to_dict() (don't forget the comma if specifying a
single field).

NOTE: If you choose to implement a Flask-RESTful app, you need to add code to
instantiate the `Api` class in server/app.py.

### GET /coffees

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "name": "Mocha"
  },
  {
    "id": 2,
    "name": "Flat White"
  },
  {
    "id": 3,
    "name": "Latte"
  }
]
```

Recall you can specify fields to include or exclude when serializing a model
instance to a dictionary using `to_dict()` (don't forget the comma if specifying
a single field).

### GET /customers/<int:id>

If the `Customer` exists, return JSON data in the format below:

```json
{
  "id": 1,
  "name": "Karen",
  "orders": [
    {
      "coffee": {
        "id": 1,
        "name": "Mocha"
      },
      "coffee_id": 1,
      "created_at": "2023-11-18 03:02:03",
      "customer_id": 1,
      "customization": "iced",
      "id": 1,
      "price": 5
    }
  ]
}
```

If the `Customer` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Customer not found"
}
```

### DELETE /coffees/<int:id>

If the `Coffee` exists, it should be removed from the database, along with
any `Order`s that are associated with it (a `Order` belongs
to a `Coffee`). If you did not set up your models to cascade deletes, you
need to delete associated `Order`s before the `Coffee` can be
deleted.

After deleting the `Coffee`, return an _empty_ response body, along with the
appropriate HTTP status code.

If the `Coffee` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "Coffee not found"
}
```

### GET /orders

Return JSON data in the format below:

```json
[
  {
    "coffee": {
      "id": 3,
      "name": "Latte"
    },
    "created_at": "2023-11-18 03:02:03",
    "customer": {
      "id": 3,
      "name": "Sanjay"
    },
    "customization": "oat milk",
    "id": 5
  },
  {
    "coffee": {
      "id": 3,
      "name": "Latte"
    },
    "created_at": "2023-11-18 03:02:03",
    "customer": {
      "id": 2,
      "name": "Abby"
    },
    "customization": "iced, oat milk",
    "id": 6
  }
]
```

### POST /orders

This route should create a new `Order` that is associated with an
existing `Coffee` and `Customer`. It should accept an object with the following
properties in the body of the request:

```json
{
  "coffee_id": 1,
  "customer_id": 3,
  "price": 5,
  "customization": "almond milk, iced"
}
```

If the `Order` is created successfully, send back a response with the
data related to the `Order`:

```json
{
  "coffee": {
    "id": 1,
    "name": "Mocha"
  },
  "coffee_id": 1,
  "created_at": "2023-11-18 03:22:39",
  "customer": {
    "id": 3,
    "name": "Sanjay"
  },
  "customer_id": 3,
  "customization": "almond milk, iced",
  "id": 7,
  "price": 5
}
```

If the `Order` is **not** created successfully due to a validation
error, return the following JSON data, along with the appropriate HTTP status
code:

```json
{
  "errors": ["validation errors"]
}
```
