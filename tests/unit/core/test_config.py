import pytest

from docuisine.core.config import env


@pytest.fixture(autouse=True)
def setup_env_monkeypatch(monkeypatch):
    monkeypatch.setattr(
        "subprocess.check_output",
        lambda cmd, stderr: {
            ("git", "rev-parse", "--short", "HEAD"): b"abc1234\n",
            ("uv", "version", "--short"): b"1.2.3\n",
        }[tuple(cmd)],
    )
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
    monkeypatch.setenv("MODE", "testing")


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


def test_mode():
    mode = env.MODE
    assert mode in {"development", "production", "testing"}
