from app.models.users import Department, User
from app.utils import hash_password, verify_password, get_user_permissions, has_permission, require_permission
from app.utils.auth import create_access_token, decode_access_token


def test_hash_and_verify_password():
    pwd = "SuperSecret123!"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(hashed, pwd)
    assert not verify_password(hashed, "wrong")


def _make_user(department):
    u = User(full_name="Test", email="perm@test.com", employee_id="EMPX",
             hashed_password=hash_password("pass"), department=department)
    return u


def test_get_user_permissions_and_has_permission():
    sales_user = _make_user(Department.SALES)
    sales_perms = get_user_permissions(sales_user)
    assert "view_clients" in sales_perms
    assert has_permission(sales_user, "manage_own_clients")
    assert not has_permission(sales_user, "manage_users")

    support_user = _make_user(Department.SUPPORT)
    assert "manage_own_events" in get_user_permissions(support_user)

    manager_user = _make_user(Department.MANAGEMENT)
    assert "manage_users" in get_user_permissions(manager_user)


def test_require_permission_decorator_allows_and_denies(capsys):
    @require_permission("manage_users")
    def dummy_action(user, value):  # ✅ 2 params : user + value
        return f"OK-{value}"

    manager = _make_user(Department.MANAGEMENT)
    sales = _make_user(Department.SALES)

    # manager OK
    result_ok = dummy_action(manager, 42)
    assert result_ok == "OK-42"

    # sales KO
    result_none = dummy_action(sales, 42)
    captured = capsys.readouterr()
    assert "Permission refusée" in captured.out
    assert result_none is None


def test_create_and_decode_access_token():
    data = {"sub": "test@example.com", "role": "SALES", "user_id": 1}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "test@example.com"
    assert payload["role"] == "SALES"


def test_decode_access_token_invalid(capsys):
    payload = decode_access_token("bad.token.value")
    captured = capsys.readouterr()
    assert payload is None
    assert "Jeton invalide" in captured.out
