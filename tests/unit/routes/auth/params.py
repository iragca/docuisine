from fastapi import status

from docuisine.schemas.enums import Role

POST_RESPONSE_1 = {"token_type": "bearer", "access_token": "testaccesstoken"}

POST_PARAMETERS = [
    # scenario, role, expected_status, expected_response
    ("success_auth", Role.PUBLIC, status.HTTP_200_OK, POST_RESPONSE_1),
    (
        "invalid_credentials",
        Role.PUBLIC,
        status.HTTP_401_UNAUTHORIZED,
        {"detail": "The provided password is invalid."},
    ),
    (
        "user_not_found",
        Role.PUBLIC,
        status.HTTP_404_NOT_FOUND,
        {"detail": "User with username 'nonexistentuser' not found."},
    ),
]
