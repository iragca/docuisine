import pytest

import docuisine.services.user as user_module


class FakeQuery:
    def __init__(self, session):
        self._session = session
        self._filters = {}

    def filter_by(self, **kwargs):
        self._filters.update(kwargs)
        return self

    def first(self):
        for u in self._session._store:
            if all(getattr(u, k) == v for k, v in self._filters.items()):
                return u
        return None

    def all(self):
        # Return a shallow copy to avoid external mutation
        return list(self._session._store)


class FakeSession:
    def __init__(self):
        self._store = []
        self._pending = []
        self._rolled_back = False
        self._committed = False
        self._id_counter = 1

    def add(self, obj):
        self._pending.append(obj)

    def commit(self):
        # Simulate unique constraint on username
        existing_usernames = {u.username for u in self._store}
        for obj in self._pending:
            if obj.username in existing_usernames:
                self.rollback()
                raise user_module.IntegrityError("Unique constraint violated", None, Exception())
        for obj in self._pending:
            if getattr(obj, "id", None) is None:
                setattr(obj, "id", self._id_counter)
                self._id_counter += 1
            self._store.append(obj)
        self._pending.clear()
        self._committed = True

    def rollback(self):
        self._rolled_back = True
        self._pending.clear()

    def query(self, _model):
        return FakeQuery(self)


@pytest.fixture
def fake_session():
    return FakeSession()


@pytest.fixture
def service(fake_session):
    return user_module.UserService(fake_session)


@pytest.fixture(autouse=True)
def patch_hash(monkeypatch):
    def _fake_hash(pw: str) -> str:
        return f"sha256::{pw}"

    monkeypatch.setattr(user_module, "hash_in_sha256", _fake_hash)


def test_create_user_success_hash_and_commit(service, fake_session):
    user = service.create_user("alice", "secret")
    assert isinstance(user, user_module.User)
    assert user.username == "alice"
    assert user.password == "sha256::secret"
    assert fake_session._committed is True
    # Ensure it was stored and has an id
    assert user in fake_session._store
    assert getattr(user, "id", None) is not None


def test_create_user_duplicate_raises_and_rollback(service, fake_session):
    u1 = service.create_user("bob", "pw1")
    assert u1.username == "bob"
    with pytest.raises(user_module.UserExistsError):
        service.create_user("bob", "pw2")
    assert fake_session._rolled_back is True
    # Only the first user exists
    assert [u.username for u in fake_session._store] == ["bob"]


def test_get_user_by_id_takes_precedence_over_username(service):
    u1 = service.create_user("charlie", "pw")
    u2 = service.create_user("charlie2", "pw")
    # Request with both id and another username; id should take precedence
    res = service.get_user(user_id=u1.id, username=u2.username)
    assert res.id == u1.id
    assert res.username == u1.username


def test_get_user_by_username_found(service):
    u = service.create_user("dora", "pw")
    res = service.get_user(username="dora")
    assert res.id == u.id
    assert res.username == "dora"


def test_get_user_without_params_raises_value_error(service):
    with pytest.raises(ValueError):
        service.get_user()


def test_get_user_not_found_by_id_raises(service):
    with pytest.raises(user_module.UserNotFoundError):
        service.get_user(user_id=9999)


def test_get_user_not_found_by_username_raises(service):
    with pytest.raises(user_module.UserNotFoundError):
        service.get_user(username="no_such_user")


def test_get_all_users_returns_list(service):
    service.create_user("eve", "1")
    service.create_user("frank", "2")
    all_users = service.get_all_users()
    assert isinstance(all_users, list)
    assert {u.username for u in all_users} == {"eve", "frank"}
