"""Test parameters for store route tests."""

from fastapi import status

# ========== GET Responses ==========

GET_ALL_STORES_RESPONSE = [
    {
        "id": 1,
        "name": "Grocery Mart",
        "address": "123 Main St",
        "longitude": None,
        "latitude": None,
        "phone": None,
        "website": None,
        "description": None,
    },
    {
        "id": 2,
        "name": "Corner Shop",
        "address": "456 Elm St",
        "longitude": None,
        "latitude": None,
        "phone": None,
        "website": None,
        "description": None,
    },
    {
        "id": 3,
        "name": "Organic Market",
        "address": "789 Oak Ave",
        "longitude": None,
        "latitude": None,
        "phone": None,
        "website": None,
        "description": None,
    },
]

GET_STORE_BY_ID_RESPONSE = {
    "id": 1,
    "name": "Supermarket",
    "address": "999 Broadway",
    "longitude": -118.2437,
    "latitude": 34.0522,
    "phone": "555-0000",
    "website": "https://supermarket.com",
    "description": "Large supermarket",
}

GET_STORE_NOT_FOUND_RESPONSE = {"detail": "Store with ID 999 not found."}

# Parametrization for GET tests
# scenario, client_name, expected_status, expected_response
GET_PARAMETERS = [
    ("get_all", "public", status.HTTP_200_OK, GET_ALL_STORES_RESPONSE),
    ("get_all", "user", status.HTTP_200_OK, GET_ALL_STORES_RESPONSE),
    ("get_all", "admin", status.HTTP_200_OK, GET_ALL_STORES_RESPONSE),
    ("get_by_id", "public", status.HTTP_200_OK, GET_STORE_BY_ID_RESPONSE),
    ("get_by_id", "user", status.HTTP_200_OK, GET_STORE_BY_ID_RESPONSE),
    ("get_by_id", "admin", status.HTTP_200_OK, GET_STORE_BY_ID_RESPONSE),
    ("get_not_found", "public", status.HTTP_404_NOT_FOUND, GET_STORE_NOT_FOUND_RESPONSE),
    ("get_not_found", "user", status.HTTP_404_NOT_FOUND, GET_STORE_NOT_FOUND_RESPONSE),
    ("get_not_found", "admin", status.HTTP_404_NOT_FOUND, GET_STORE_NOT_FOUND_RESPONSE),
]

# ========== POST Responses ==========

POST_RESPONSE_1 = {
    "id": 1,
    "name": "New Store",
    "address": "111 First St",
    "longitude": None,
    "latitude": None,
    "phone": None,
    "website": None,
    "description": "Nice store",
}
POST_RESPONSE_2 = {
    "id": 2,
    "name": "Mini",
    "address": "222 Second St",
    "longitude": None,
    "latitude": None,
    "phone": None,
    "website": None,
    "description": None,
}
POST_RESPONSE_CONFLICT = {"detail": "Store with name 'Existing Store' already exists."}

# Parametrization for POST tests
# client_name, expected_status, expected_response
POST_PARAMETERS = [
    ("user", status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("admin", status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("user", status.HTTP_201_CREATED, POST_RESPONSE_2),
    ("admin", status.HTTP_201_CREATED, POST_RESPONSE_2),
    ("user", status.HTTP_409_CONFLICT, POST_RESPONSE_CONFLICT),
    ("admin", status.HTTP_409_CONFLICT, POST_RESPONSE_CONFLICT),
]

# ========== PUT Responses ==========

PUT_RESPONSE_FULL = {
    "id": 1,
    "name": "Updated Store",
    "address": "Updated Address",
    "longitude": None,
    "latitude": None,
    "phone": "555-9999",
    "website": "https://updated.com",
    "description": "Updated description",
}
PUT_RESPONSE_PARTIAL = {
    "id": 1,
    "name": "Shop",
    "address": "New Address",
    "longitude": None,
    "latitude": None,
    "phone": None,
    "website": None,
    "description": None,
}
PUT_RESPONSE_NOT_FOUND = {"detail": "Store with ID 999 not found."}
PUT_RESPONSE_CONFLICT = {"detail": "Store with name 'Existing Store' already exists."}

# Parametrization for PUT tests
# scenario, client_name, input_data, expected_status, expected_response
PUT_PARAMETERS = [
    (
        "update_full",
        "user",
        {
            "name": "Updated Store",
            "address": "Updated Address",
            "phone": "555-9999",
            "website": "https://updated.com",
            "description": "Updated description",
        },
        status.HTTP_200_OK,
        PUT_RESPONSE_FULL,
    ),
    (
        "update_partial",
        "user",
        {"address": "New Address"},
        status.HTTP_200_OK,
        PUT_RESPONSE_PARTIAL,
    ),
    (
        "not_found",
        "user",
        {"name": "New Name"},
        status.HTTP_404_NOT_FOUND,
        PUT_RESPONSE_NOT_FOUND,
    ),
    (
        "conflict",
        "user",
        {"name": "Existing Store"},
        status.HTTP_409_CONFLICT,
        PUT_RESPONSE_CONFLICT,
    ),
]

# ========== DELETE Responses ==========

DELETE_RESPONSE_SUCCESS = {"detail": "Store with ID 1 has been deleted."}
DELETE_RESPONSE_NOT_FOUND = {"detail": "Store with ID 999 not found."}

# Parametrization for DELETE tests
# scenario, client_name, store_id, expected_status, expected_response
DELETE_PARAMETERS = [
    ("delete_success", "user", 1, status.HTTP_200_OK, DELETE_RESPONSE_SUCCESS),
    ("delete_not_found", "user", 999, status.HTTP_404_NOT_FOUND, DELETE_RESPONSE_NOT_FOUND),
]
