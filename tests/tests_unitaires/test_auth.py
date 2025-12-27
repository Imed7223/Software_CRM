from app.utils import auth
from app.models.users import Department, User


def test_hash_and_verify_password():
    pwd = "SuperSecret123!"
    hashed = auth.hash_password(pwd)

    assert hashed != pwd
    assert auth.verify_password(hashed, pwd)
    assert auth.verify_password(hashed, "wrong") is False


def _make_user(department):
    u = User(
        full_name="Test",
        email="perm@test.com",
        employee_id="EMPX",
        hashed_password=auth.hash_password("pass"),
        department=department,
    )
    return u


def test_get_user_permissions_and_has_permission():
    sales_user = _make_user(Department.SALES)
    support_user = _make_user(Department.SUPPORT)
    manager_user = _make_user(Department.MANAGEMENT)

    sales_perms = auth.get_user_permissions(sales_user)
    assert "view_clients" in sales_perms
    assert auth.has_permission(sales_user, "manage_clients") is True
    assert auth.has_permission(sales_user, "manage_users") is False

    support_perms = auth.get_user_permissions(support_user)
    assert "manage_events" in support_perms

    manager_perms = auth.get_user_permissions(manager_user)
    assert "manage_users" in manager_perms

    unknown_user = _make_user(None)
    assert auth.get_user_permissions(unknown_user) == []


def test_require_permission_decorator_allows_and_denies(capsys):
    @auth.require_permission("manage_users")
    def dummy_action(user, value):
        return f"OK-{value}"

    manager = _make_user(Department.MANAGEMENT)
    sales = _make_user(Department.SALES)

    # autorisé
    result_ok = dummy_action(manager, 42)
    assert result_ok == "OK-42"

    # refusé
    result_none = dummy_action(sales, 42)
    captured = capsys.readouterr()
    assert "Permission refusée" in captured.out
    assert result_none is None


def test_create_and_decode_access_token():
    data = {"sub": "test@example.com", "role": "SALES", "user_id": 1}
    token = auth.create_access_token(data)

    payload = auth.decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "test@example.com"
    assert payload["role"] == "SALES"
    assert payload["user_id"] == 1


def test_decode_access_token_invalid(capsys):
    payload = auth.decode_access_token("bad.token.value")
    captured = capsys.readouterr()
    assert payload is None
    assert "Jeton invalide" in captured.out
