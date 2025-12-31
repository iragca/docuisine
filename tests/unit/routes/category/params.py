from fastapi import status

from docuisine.schemas.enums import Role

FORBIDDEN_ACCESS_RESPONSE = {"detail": "You do not have permission to perform this action."}
UNAUTHORIZED_ACCESS_RESPONSE = {"detail": "Not authenticated"}


# ---------------- GET PARAMETERS ----------------
GET_ALL_CATEGORIES_RESPONSE = [
    {
        "id": 1,
        "name": "Dessert",
        "description": "Sweet treats",
        "img": None,
        "preview_img": None,
    },
    {
        "id": 2,
        "name": "Vegetarian",
        "description": "Meat-free dishes",
        "img": None,
        "preview_img": None,
    },
    {
        "id": 3,
        "name": "Quick Meals",
        "description": None,
        "img": None,
        "preview_img": None,
    },
]

GET_BY_ID_RESPONSE = {
    "id": 1,
    "name": "Dessert",
    "description": "Sweet treats",
    "img": None,
    "preview_img": None,
}

GET_NOT_FOUND_RESPONSE = {"detail": "Category with ID 999 not found."}


GET_PARAMETERS = [
    # scenario, role, expected_status, expected_response
    ("get_all", Role.PUBLIC, status.HTTP_200_OK, GET_ALL_CATEGORIES_RESPONSE),
    ("get_all", Role.USER, status.HTTP_200_OK, GET_ALL_CATEGORIES_RESPONSE),
    ("get_all", Role.ADMIN, status.HTTP_200_OK, GET_ALL_CATEGORIES_RESPONSE),
    ("get_by_id", Role.PUBLIC, status.HTTP_200_OK, GET_BY_ID_RESPONSE),
    ("get_by_id", Role.USER, status.HTTP_200_OK, GET_BY_ID_RESPONSE),
    ("get_by_id", Role.ADMIN, status.HTTP_200_OK, GET_BY_ID_RESPONSE),
    ("get_not_found", Role.PUBLIC, status.HTTP_404_NOT_FOUND, GET_NOT_FOUND_RESPONSE),
    ("get_not_found", Role.USER, status.HTTP_404_NOT_FOUND, GET_NOT_FOUND_RESPONSE),
    ("get_not_found", Role.ADMIN, status.HTTP_404_NOT_FOUND, GET_NOT_FOUND_RESPONSE),
]


# ---------------- POST PARAMETERS ----------------

POST_RESPONSE_1 = {
    "name": "Appetizer",
    "description": "Starters",
    "id": 4,
    "img": None,
    "preview_img": None,
}
POST_RESPONSE_2 = {
    "name": "Appetizer",
    "description": None,
    "id": 4,
    "img": None,
    "preview_img": None,
}
POST_RESPONSE_3 = {"detail": "Category with name 'Dessert' already exists."}
POST_RESPONSE_IMAGE_UPLOAD = {
    "name": "Appetizer",
    "description": "Starters",
    "id": 4,
    "img": "appetizer_full.jpg",
    "preview_img": "appetizer_preview.jpg",
}

POST_PARAMETERS = [
    # scenario, role, expected_status, expected_response
    ("unauthorized", Role.PUBLIC, status.HTTP_401_UNAUTHORIZED, UNAUTHORIZED_ACCESS_RESPONSE),
    ("unauthorized", Role.USER, status.HTTP_403_FORBIDDEN, FORBIDDEN_ACCESS_RESPONSE),
    ("success", Role.ADMIN, status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("success_no_description", Role.ADMIN, status.HTTP_201_CREATED, POST_RESPONSE_2),
    (
        "conflict",
        Role.ADMIN,
        status.HTTP_409_CONFLICT,
        POST_RESPONSE_3,
    ),
    ("success_image_upload", Role.ADMIN, status.HTTP_201_CREATED, POST_RESPONSE_IMAGE_UPLOAD),
]

# ---------------- PUT PARAMETERS ----------------
PUT_PARAMETERS = [
    # scenario, role, expected_status, expected_response
    (
        "unauthorized",
        Role.PUBLIC,
        status.HTTP_401_UNAUTHORIZED,
        UNAUTHORIZED_ACCESS_RESPONSE,
    ),
    (
        "unauthorized",
        Role.USER,
        status.HTTP_403_FORBIDDEN,
        FORBIDDEN_ACCESS_RESPONSE,
    ),
    (
        "update_success",
        Role.ADMIN,
        status.HTTP_200_OK,
        {
            "id": 1,
            "name": "Desserts",
            "description": "Updated description",
            "img": "test",
            "preview_img": "test",
        },
    ),
    (
        "update_name_only",
        Role.ADMIN,
        status.HTTP_200_OK,
        {
            "id": 1,
            "name": "Updated Name",
            "description": "Original description",
            "img": None,
            "preview_img": None,
        },
    ),
    (
        "update_not_found",
        Role.ADMIN,
        status.HTTP_404_NOT_FOUND,
        {"detail": "Category with ID 1 not found."},
    ),
    (
        "update_conflict",
        Role.ADMIN,
        status.HTTP_409_CONFLICT,
        {"detail": "Category with name 'Dessert' already exists."},
    )
]

# ---------------- DELETE PARAMETERS ----------------
DELETE_PARAMETERS = [
    # scenario, role, category_id, expected_status, expected_response
    (
        "unauthorized",
        Role.PUBLIC,
        1,
        status.HTTP_401_UNAUTHORIZED,
        UNAUTHORIZED_ACCESS_RESPONSE,
    ),
    (
        "unauthorized",
        Role.USER,
        1,
        status.HTTP_403_FORBIDDEN,
        FORBIDDEN_ACCESS_RESPONSE,
    ),
    (
        "delete_success",
        Role.ADMIN,
        1,
        status.HTTP_200_OK,
        {"detail": "Category with ID 1 has been deleted."},
    ),
    (
        "delete_not_found",
        Role.ADMIN,
        999,
        status.HTTP_404_NOT_FOUND,
        {"detail": "Category with ID 999 not found."},
    ),
]
