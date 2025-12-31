"""Test parameters for recipe route tests."""

from fastapi import status

# ========== GET Responses ==========

GET_ALL_RECIPES_RESPONSE = [
    {
        "id": 1,
        "user_id": 1,
        "name": "Pasta Carbonara",
        "description": None,
        "prep_time_sec": None,
        "cook_time_sec": None,
        "non_blocking_time_sec": None,
        "servings": None,
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "Chicken Curry",
        "prep_time_sec": 900,
        "description": None,
        "cook_time_sec": 1800,
        "non_blocking_time_sec": None,
        "servings": None,
    },
    {
        "id": 3,
        "user_id": 2,
        "name": "Vegan Tacos",
        "prep_time_sec": None,
        "description": None,
        "cook_time_sec": None,
        "non_blocking_time_sec": None,
        "servings": 4,
    },
]

GET_RECIPE_BY_ID_RESPONSE = {
    "id": 1,
    "user_id": 1,
    "name": "Beef Stew",
    "description": None,
    "prep_time_sec": 1200,
    "cook_time_sec": 7200,
    "non_blocking_time_sec": 8400,
    "servings": 6,
}

GET_RECIPE_NOT_FOUND_RESPONSE = {"detail": "Recipe with ID 999 not found."}

# Parametrization for GET tests
# scenario, client_name, expected_status, expected_response
GET_PARAMETERS = [
    ("get_all", "public", status.HTTP_200_OK, GET_ALL_RECIPES_RESPONSE),
    ("get_all", "user", status.HTTP_200_OK, GET_ALL_RECIPES_RESPONSE),
    ("get_all", "admin", status.HTTP_200_OK, GET_ALL_RECIPES_RESPONSE),
    ("get_by_id", "public", status.HTTP_200_OK, GET_RECIPE_BY_ID_RESPONSE),
    ("get_by_id", "user", status.HTTP_200_OK, GET_RECIPE_BY_ID_RESPONSE),
    ("get_by_id", "admin", status.HTTP_200_OK, GET_RECIPE_BY_ID_RESPONSE),
    ("get_not_found", "public", status.HTTP_404_NOT_FOUND, GET_RECIPE_NOT_FOUND_RESPONSE),
    ("get_not_found", "user", status.HTTP_404_NOT_FOUND, GET_RECIPE_NOT_FOUND_RESPONSE),
    ("get_not_found", "admin", status.HTTP_404_NOT_FOUND, GET_RECIPE_NOT_FOUND_RESPONSE),
]

# ========== POST Responses ==========

POST_RESPONSE_1 = {
    "id": 1,
    "user_id": 1,
    "name": "Chocolate Cake",
    "description": None,
    "prep_time_sec": 1800,
    "cook_time_sec": 2700,
    "non_blocking_time_sec": None,
    "servings": 8,
}

POST_RESPONSE_2 = {
    "id": 2,
    "user_id": 2,
    "name": "Simple Salad",
    "description": None,
    "prep_time_sec": None,
    "cook_time_sec": None,
    "non_blocking_time_sec": None,
    "servings": None,
}
POST_RESPONSE_CONFLICT = {"detail": "Recipe with name 'Existing Recipe' already exists."}

# Parametrization for POST tests
# client_name, expected_status, expected_response
POST_PARAMETERS = [
    ("user", status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("admin", status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("user", status.HTTP_201_CREATED, POST_RESPONSE_2),
    ("admin", status.HTTP_201_CREATED, POST_RESPONSE_2),
    ("admin", status.HTTP_409_CONFLICT, POST_RESPONSE_CONFLICT),
]

# ========== PUT Responses ==========

PUT_RESPONSE_FULL = {
    "id": 1,
    "user_id": 1,
    "name": "Updated Recipe",
    "description": None,
    "prep_time_sec": 1500,
    "cook_time_sec": 2400,
    "non_blocking_time_sec": 3900,
    "servings": 4,
}
PUT_RESPONSE_PARTIAL = {
    "id": 1,
    "user_id": 1,
    "name": "Original Name",
    "description": None,
    "prep_time_sec": None,
    "cook_time_sec": None,
    "non_blocking_time_sec": None,
    "servings": 10,
}
PUT_RESPONSE_NOT_FOUND = {"detail": "Recipe with ID 999 not found."}
PUT_RESPONSE_CONFLICT = {"detail": "Recipe with name 'Existing Recipe' already exists."}

# Parametrization for PUT tests
# scenario, client_name, input_data, expected_status, expected_response
PUT_PARAMETERS = [
    (
        "update_full",
        "admin",
        {
            "name": "Updated Recipe",
            "prep_time_sec": 1500,
            "cook_time_sec": 2400,
            "non_blocking_time_sec": 3900,
            "servings": 4,
        },
        status.HTTP_200_OK,
        PUT_RESPONSE_FULL,
    ),
    (
        "update_partial",
        "admin",
        {"servings": 10},
        status.HTTP_200_OK,
        PUT_RESPONSE_PARTIAL,
    ),
    (
        "not_found",
        "admin",
        {"name": "New Name"},
        status.HTTP_404_NOT_FOUND,
        PUT_RESPONSE_NOT_FOUND,
    ),
    (
        "conflict",
        "admin",
        {"name": "Existing Recipe"},
        status.HTTP_409_CONFLICT,
        PUT_RESPONSE_CONFLICT,
    ),
]

# ========== DELETE Responses ==========

DELETE_RESPONSE_SUCCESS = {"detail": "Recipe with ID 1 has been deleted."}
DELETE_RESPONSE_NOT_FOUND = {"detail": "Recipe with ID 999 not found."}

# Parametrization for DELETE tests
# scenario, client_name, recipe_id, expected_status, expected_response
DELETE_PARAMETERS = [
    ("delete_success", "admin", 1, status.HTTP_200_OK, DELETE_RESPONSE_SUCCESS),
    ("delete_not_found", "admin", 999, status.HTTP_404_NOT_FOUND, DELETE_RESPONSE_NOT_FOUND),
]
