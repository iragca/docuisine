from docuisine.core.config import env


def test_database_url():
    assert isinstance(env.DATABASE_URL, str)
    assert env.DATABASE_URL.startswith("postgresql")


def test_commit_hash():
    commit_hash = env.COMMIT_HASH
    assert commit_hash is not None
    assert isinstance(commit_hash, str)
    assert len(commit_hash) == 7  # Short commit hash length


def test_version():
    version = env.VERSION
    assert version is not None
    assert isinstance(version, str)
    assert version.count(".") == 2  # Basic check for version format
