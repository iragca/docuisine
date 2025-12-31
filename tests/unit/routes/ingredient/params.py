from fastapi import status

# Define expected responses
GET_INGREDIENTS_RESPONSE = [
    {"id": 1, "name": "Sugar", "description": "White sugar", "recipe_id": None},
    {"id": 2, "name": "Flour", "description": "All-purpose flour", "recipe_id": None},
    {"id": 3, "name": "Salt", "description": None, "recipe_id": None},
]

GET_INGREDIENT_BY_ID_RESPONSE = {
    "id": 1,
    "name": "Butter",
    "description": "Unsalted butter",
    "recipe_id": None,
}
GET_INGREDIENT_NOT_FOUND_RESPONSE = {"detail": "Ingredient with ID 999 not found."}

# Parametrization for GET tests
GET_PARAMETERS = [
    # scenario, client_name, expected_status, expected_response
    ("get_all", "public", status.HTTP_200_OK, GET_INGREDIENTS_RESPONSE),
    ("get_all", "user", status.HTTP_200_OK, GET_INGREDIENTS_RESPONSE),
    ("get_all", "admin", status.HTTP_200_OK, GET_INGREDIENTS_RESPONSE),
    ("get_by_id", "public", status.HTTP_200_OK, GET_INGREDIENT_BY_ID_RESPONSE),
    ("get_by_id", "user", status.HTTP_200_OK, GET_INGREDIENT_BY_ID_RESPONSE),
    ("get_by_id", "admin", status.HTTP_200_OK, GET_INGREDIENT_BY_ID_RESPONSE),
    ("get_not_found", "public", status.HTTP_404_NOT_FOUND, GET_INGREDIENT_NOT_FOUND_RESPONSE),
    ("get_not_found", "user", status.HTTP_404_NOT_FOUND, GET_INGREDIENT_NOT_FOUND_RESPONSE),
    ("get_not_found", "admin", status.HTTP_404_NOT_FOUND, GET_INGREDIENT_NOT_FOUND_RESPONSE),
]


POST_RESPONSE_1 = {"name": "Eggs", "description": "Large eggs", "id": 1, "recipe_id": None}
POST_RESPONSE_2 = {"name": "Eggs", "description": None, "id": 1, "recipe_id": None}
POST_RESPONSE_3 = {"name": "Eggs", "description": "Large eggs", "id": 1, "recipe_id": 5}
POST_RESPONSE_4 = {"detail": "Ingredient with name 'Eggs' already exists."}


POST_PARAMETERS = [
    ("user", status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("admin", status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("user", status.HTTP_201_CREATED, POST_RESPONSE_2),
    ("admin", status.HTTP_201_CREATED, POST_RESPONSE_2),
    ("user", status.HTTP_201_CREATED, POST_RESPONSE_3),
    ("admin", status.HTTP_201_CREATED, POST_RESPONSE_3),
    ("user", status.HTTP_409_CONFLICT, POST_RESPONSE_4),
    ("admin", status.HTTP_409_CONFLICT, POST_RESPONSE_4),
]

# Define PUT test scenarios
PUT_PARAMETERS = [
    # scenario, client_name, input_data, expected_status, expected_response
    (
        "update_full",
        "admin",
        {"name": "Brown Sugar", "description": "Updated description"},
        status.HTTP_200_OK,
        {"id": 1, "name": "Brown Sugar", "description": "Updated description", "recipe_id": None},
    ),
    (
        "update_partial",
        "admin",
        {"name": "Updated Name"},
        status.HTTP_200_OK,
        {
            "id": 1,
            "name": "Updated Name",
            "description": "Original description",
            "recipe_id": None,
        },
    ),
    (
        "update_recipe_id",
        "admin",
        {"recipe_id": 10},
        status.HTTP_200_OK,
        {"id": 1, "name": "Dough", "description": "Pizza dough", "recipe_id": 10},
    ),
    (
        "not_found",
        "admin",
        {"name": "New Name"},
        status.HTTP_404_NOT_FOUND,
        {"detail": "Ingredient with ID 999 not found."},
    ),
    (
        "conflict",
        "admin",
        {"name": "Existing"},
        status.HTTP_409_CONFLICT,
        {"detail": "Ingredient with name 'Existing' already exists."},
    ),
]

# Define DELETE test scenarios
DELETE_PARAMETERS = [
    # scenario, client_name, ingredient_id, expected_status, expected_response
    (
        "delete_success",
        "admin",
        1,
        status.HTTP_200_OK,
        {"detail": "Ingredient with ID 1 has been deleted."},
    ),
    (
        "delete_not_found",
        "admin",
        999,
        status.HTTP_404_NOT_FOUND,
        {"detail": "Ingredient with ID 999 not found."},
    ),
]
