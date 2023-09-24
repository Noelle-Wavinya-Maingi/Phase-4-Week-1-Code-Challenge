# Flask Code Challenge - Pizza Restaurants

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)

This is a project creating a FLASK API for a Pizza Restaurant domain.

Running the Flask server and using Postman to make requests
Models.

## Setup

Before running the application, make sure to set up your development environment and install the required dependencies using:

```bash
pip install -r requirements.txt
```

## Models

You need to create the following relationships:

- A Restaurant has many Pizzas through RestaurantPizza
- A Pizza has many Restaurants through RestaurantPizza
- A RestaurantPizza belongs to a Restaurant and belongs to a Pizza

![img.png](https://moringa.instructure.com/courses/498/files/325552/preview)

## Validations

Add validations to the RestaurantPizza model:

- Must have a price between 1 and 30

Add validations to Restaurant Model:

- must have a name less than 50 words in length
- must have a unique name

## Routes

Implement the following routes. Make sure to return JSON data in the specified format along with the appropriate HTTP verb.

### GET /restaurants

Return JSON data in the format below:

```bash
[
  {
    "id": 1,
    "name": "Dominion Pizza",
    "address": "Good Italian, Ngong Road, 5th Avenue"
  },
  {
    "id": 2,
    "name": "Pizza Hut",
    "address": "Westgate Mall, Mwanzi Road, Nrb 100"
  }
]
```

### GET /restaurants/:id

If the Restaurant exists, return JSON data in the format below:

```bash
{
  "id": 1,
  "name": "Dominion Pizza",
  "address": "Good Italian, Ngong Road, 5th Avenue",
  "pizzas": [
    {
      "id": 1,
      "name": "Cheese",
      "ingredients": "Dough, Tomato Sauce, Cheese"
    },
    {
      "id": 2,
      "name": "Pepperoni",
      "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
    }
  ]
}
```

If the Restaurant does not exist, return the following JSON data, along with the appropriate HTTP status code:

```bash
{
  "error": "Restaurant not found"
}
```

### DELETE /restaurants/:id

If the Restaurant exists, remove it from the database, along with any associated RestaurantPizzas. After deleting the Restaurant, return an empty response body with the appropriate HTTP status code.

If the Restaurant does not exist, return the following JSON data, along with the appropriate HTTP status code:

```bash
{
  "error": "Restaurant not found"
}
```

### GET /pizzas

Return JSON data in the format below:

```bash
[
  {
    "id": 1,
    "name": "Cheese",
    "ingredients": "Dough, Tomato Sauce, Cheese"
  },
  {
    "id": 2,
    "name": "Pepperoni",
    "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
  }
]
```

### POST /restaurant_pizzas

This route should create a new RestaurantPizza associated with an existing Pizza and Restaurant. It should accept an object with the following properties in the body of the request:

```bash
{
  "price": 5,
  "pizza_id": 1,
  "restaurant_id": 3
}
```

If the RestaurantPizza is created successfully, send back a response with the data related to the Pizza:

```bash
{
  "id": 1,
  "name": "Cheese",
  "ingredients": "Dough, Tomato Sauce, Cheese"
}
```

If the RestaurantPizza is not created successfully, return the following JSON data, along with the appropriate HTTP status code:

```bash
{
  "errors": ["validation errors"]
}
```

## Testing

To test your endpoints, you can run the Flask server and use Postman or any other HTTP client to make requests.

```bash
flask run
```

Make sure to set up your database and configuration as needed for testing.

## Author

The author of the code challenge solution is [Noelle Maingi.](https://github.com/Noelle-Wavinya-Maingi)
