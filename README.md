# CarFord API Documentation

## Overview

This API provides endpoints for managing cars and car owners in the Nork-Town system. It allows users to perform CRUD operations on car records and manage the relationship between cars and their owners. Cars have constraints on their color and model, and each owner can have up to three cars.

## Dependencies

+ [Docker](https://www.docker.com/) : a containerization platform for building, packaging, and distributing applications.
+ [Docker Compose](https://docs.docker.com/compose/) : a tool for defining and running multi-container Docker applications.

## Running

Clone repository

```bash
git clone 
```

Execute the command

```bash
docker-compose up
```

And run the commands

```bash
make migrations
make migrate
```

To run the tests

```bash
make test
```

## Base URL

```
http://localhost:5000/api
```

## Endpoints

### 1. **Get All Cars**

**Endpoint:** `GET /cars`

**Description:** Retrieves a list of all cars with optional filtering and pagination.

**Query Parameters:**
- `color` (optional) - Filter by car color.
- `model` (optional) - Filter by car model.
- `limit` (optional) - Limit the number of results returned.
- `offset` (optional) - Offset the results by a number of records.

**Response:**
```json
{
    "count": 2,
    "cars": [
        {
            "id": 1,
            "color": "blue",
            "model": "hatch",
            "owner_id": 1
        },
        {
            "id": 2,
            "color": "yellow",
            "model": "sedan",
            "owner_id": 2
        }
    ]
}
```

### 2. **Get a Single Car**

**Endpoint:** `GET /cars/{car_id}`

**Description:** Retrieves details of a specific car by its ID.

**Parameters:**
- `car_id` - ID of the car to retrieve.

**Response:**
```json
{
    "id": 1,
    "color": "blue",
    "model": "hatch",
    "owner_id": 1
}
```

### 3. **Create a New Car**

**Endpoint:** `POST /cars`

**Description:** Creates a new car record.

**Request Body:**
```json
{
    "color": "blue",
    "model": "hatch",
    "owner_id": 1
}
```

**Response:**
```json
{
    "id": 1,
    "color": "blue",
    "model": "hatch",
    "owner_id": 1
}
```

**Errors:**
- `400 Bad Request` - If the provided data is invalid or the owner does not exist.

### 4. **Update an Existing Car**

**Endpoint:** `PUT /cars/{car_id}`

**Description:** Updates an existing car record by its ID.

**Parameters:**
- `car_id` - ID of the car to update.

**Request Body:**
```json
{
    "color": "gray",
    "model": "convertible",
    "owner_id": 2
}
```

**Response:**
```json
{
    "id": 1,
    "color": "gray",
    "model": "convertible",
    "owner_id": 2
}
```

**Errors:**
- `404 Not Found` - If the car does not exist.

### 5. **Delete a Car**

**Endpoint:** `DELETE /cars/{car_id}`

**Description:** Deletes a car record by its ID.

**Parameters:**
- `car_id` - ID of the car to delete.

**Response:**
```json
{
    "id": 1,
    "color": "gray",
    "model": "convertible",
    "owner_id": 2
}
```

**Errors:**
- `404 Not Found` - If the car does not exist.

### 6. **Get All Owners**

**Endpoint:** `GET /owners`

**Description:** Retrieves a list of all car owners.

**Response:**
```json
{
    "count": 2,
    "owners": [
        {
            "id": 1,
            "name": "John Doe",
            "sale_opportunity": false,
            "cars": [
                {
                    "id": 2,
                    "color": "blue",
                    "model": "sedan"
                },
                {
                    "id": 4,
                    "color": "blue",
                    "model": "sedan"
                }
            ]
        },
        {
            "id": 2,
            "name": "John Doe",
            "sale_opportunity": false,
            "cars": [
                {
                    "id": 3,
                    "color": "blue",
                    "model": "sedan"
                }
            ]
        }
    ]
}
```

### 7. **Get a Single Owner**

**Endpoint:** `GET /owners/{owner_id}`

**Description:** Retrieves details of a specific owner by their ID.

**Parameters:**
- `owner_id` - ID of the owner to retrieve.

**Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "sale_oportunity": true,
    "cars": []
}
```

### 8. **Create a New Owner**

**Endpoint:** `POST /owners`

**Description:** Creates a new owner record.

**Request Body:**
```json
{
    "name": "Alice Johnson",
}
```

**Response:**
```json
{
    "id": 3,
    "name": "Alice Johnson",
    "sale_oportunity": true,
    "cars": []
}
```

### 9. **Update an Existing Owner**

**Endpoint:** `PUT /owners/{owner_id}`

**Description:** Updates an existing owner record by their ID.

**Parameters:**
- `owner_id` - ID of the owner to update.

**Request Body:**
```json
{
    "name": "Alice Johnson",
}
```

**Response:**
```json
{
    "id": 3,
    "name": "Alice Johnson",
    "sale_oportunity": true,
    "cars": []
}
```

**Errors:**
- `404 Not Found` - If the owner does not exist.

### 10. **Delete an Owner**

**Endpoint:** `DELETE /owners/{owner_id}`

**Description:** Deletes an owner record by their ID. This will also delete all cars associated with this owner.

**Parameters:**
- `owner_id` - ID of the owner to delete.

**Response:**
```json
{
    "id": 3,
    "name": "Alice Johnson",
    "sale_oportunity": true,
    "cars": []
}
```

**Errors:**
- `404 Not Found` - If the owner does not exist.

## Enum Values

### Color Enum

- `yellow`
- `blue`
- `gray`

### Model Enum

- `hatch`
- `sedan`
- `convertible`

## Error Responses

- `400 Bad Request` - The request was invalid or cannot be served. This error is usually caused by incorrect request data.
- `404 Not Found` - The requested resource could not be found.

---