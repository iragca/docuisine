from docuisine.utils.hashing import hash_in_sha256


def test_hash_in_sha256():
    test_string = "testpassword"
    expected_hash = "9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05"
    hash_result = hash_in_sha256(test_string)
    assert hash_result == expected_hash
