"""Test parameters for user route tests."""

from fastapi import status

FORBIDDEN_ACCESS_RESPONSE = {"detail": "You do not have permission to perform this action."}
UNAUTHORIZED_ACCESS_RESPONSE = {"detail": "Not authenticated"}

# ========== GET Responses ==========

GET_ALL_USERS_RESPONSE = [
    {
        "id": 1,
        "username": "user1",
        "email": None,
        "created_at": None,
        "img": None,
        "updated_at": None,
        "preview_img": None,
    },
    {
        "id": 2,
        "username": "user2",
        "email": None,
        "created_at": None,
        "img": None,
        "updated_at": None,
        "preview_img": None,
    },
]

GET_USER_NOT_FOUND_RESPONSE = {"detail": "User with ID 999 not found."}

# Parametrization for GET tests
# scenario, client_name, expected_status, expected_response
GET_PARAMETERS = [
    ("get_all", "public", status.HTTP_200_OK, GET_ALL_USERS_RESPONSE),
    ("get_all", "user", status.HTTP_200_OK, GET_ALL_USERS_RESPONSE),
    ("get_all", "admin", status.HTTP_200_OK, GET_ALL_USERS_RESPONSE),
    ("get_not_found", "public", status.HTTP_404_NOT_FOUND, GET_USER_NOT_FOUND_RESPONSE),
    ("get_not_found", "user", status.HTTP_404_NOT_FOUND, GET_USER_NOT_FOUND_RESPONSE),
    ("get_not_found", "admin", status.HTTP_404_NOT_FOUND, GET_USER_NOT_FOUND_RESPONSE),
]

# ========== POST Responses ==========

POST_RESPONSE_1 = {
    "id": 1,
    "username": "newuser",
    "email": None,
    "preview_img": None,
    "created_at": None,
    "img": None,
    "updated_at": None,
}
POST_RESPONSE_2 = {
    "id": 1,
    "username": "newuser",
    "email": "newuser@example.com",
    "preview_img": None,
    "created_at": None,
    "img": None,
    "updated_at": None,
}
POST_RESPONSE_CONFLICT = {"detail": "User with username 'user1' already exists."}

# Parametrization for POST tests
# client_name, expected_status, expected_response
POST_PARAMETERS = [
    ("public", status.HTTP_201_CREATED, POST_RESPONSE_1),
    ("public", status.HTTP_201_CREATED, POST_RESPONSE_2),
    ("public", status.HTTP_409_CONFLICT, POST_RESPONSE_CONFLICT),
]

# ========== PUT Responses ==========

PUT_RESPONSE_PASSWORD_SUCCESS = {
    "id": 1,
    "username": "existinguser",
    "email": None,
    "created_at": None,
    "img": None,
    "updated_at": None,
    "preview_img": None,
}
PUT_RESPONSE_PASSWORD_NOT_FOUND = {"detail": "User with ID 1 not found."}
PUT_RESPONSE_EMAIL_SUCCESS = {
    "id": 1,
    "username": "existinguser",
    "email": "newemail@example.com",
    "created_at": None,
    "img": None,
    "updated_at": None,
    "preview_img": None,
}
PUT_RESPONSE_EMAIL_NOT_FOUND = {"detail": "User with ID 1 not found."}
PUT_RESPONSE_EMAIL_CONFLICT = {
    "detail": "Email 'newemail@example.com' is already associated with another user."
}

# Parametrization for PUT tests
# scenario, client_name, input_data, expected_status, expected_response
PUT_PARAMETERS = [
    (
        "update_password_success",
        "user",
        {
            "id": 1,
            "old_password": "OldPassword!23",
            "new_password": "NewSecurePassword!45",
            "created_at": None,
            "img": None,
            "updated_at": None,
            "preview_img": None,
        },
        status.HTTP_200_OK,
        PUT_RESPONSE_PASSWORD_SUCCESS,
    ),
    (
        "update_password_not_found",
        "user",
        {"id": 1, "old_password": "OldPassword!23", "new_password": "NewSecurePassword!45"},
        status.HTTP_404_NOT_FOUND,
        PUT_RESPONSE_PASSWORD_NOT_FOUND,
    ),
    (
        "update_email_success",
        "user",
        {
            "id": 1,
            "password": "CurrentPassword!23",
            "email": "newemail@example.com",
            "created_at": None,
            "img": None,
            "updated_at": None,
            "preview_img": None,
        },
        status.HTTP_200_OK,
        PUT_RESPONSE_EMAIL_SUCCESS,
    ),
    (
        "update_email_not_found",
        "user",
        {
            "id": 1,
            "password": "CurrentPassword!23",
            "email": "newemail@example.com",
            "created_at": None,
            "img": None,
            "updated_at": None,
            "preview_img": None,
        },
        status.HTTP_404_NOT_FOUND,
        PUT_RESPONSE_EMAIL_NOT_FOUND,
    ),
    (
        "update_email_conflict",
        "user",
        {
            "id": 1,
            "password": "CurrentPassword!23",
            "email": "newemail@example.com",
            "created_at": None,
            "img": None,
            "updated_at": None,
            "preview_img": None,
        },
        status.HTTP_409_CONFLICT,
        PUT_RESPONSE_EMAIL_CONFLICT,
    ),
]

# ========== DELETE Responses ==========

DELETE_RESPONSE_SUCCESS = {"detail": "User with ID 1 has been deleted."}
DELETE_RESPONSE_NOT_FOUND = {"detail": "User with ID 1 not found."}

# Parametrization for DELETE tests
# scenario, client_name, user_id, expected_status, expected_response
DELETE_PARAMETERS = [
    ("unauthorized", "public", 1, status.HTTP_401_UNAUTHORIZED, UNAUTHORIZED_ACCESS_RESPONSE),
    ("delete_success", "admin", 1, status.HTTP_200_OK, DELETE_RESPONSE_SUCCESS),
    ("delete_success", "user", 1, status.HTTP_200_OK, DELETE_RESPONSE_SUCCESS),
    ("delete_not_found", "user", 1, status.HTTP_404_NOT_FOUND, DELETE_RESPONSE_NOT_FOUND),
]
