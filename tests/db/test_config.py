from docuisine.core.config import Environment


def test_database_url():
    assert isinstance(Environment.DATABASE_URL, str)
    assert Environment.DATABASE_URL.startswith("postgresql")


def test_commit_hash():
    commit_hash = Environment.COMMIT_HASH
    assert commit_hash is not None
    assert isinstance(commit_hash, str)
    assert len(commit_hash) == 7  # Short commit hash length


def test_version():
    version = Environment.VERSION
    assert version is not None
    assert isinstance(version, str)
    assert version.count(".") == 2  # Basic check for version format
