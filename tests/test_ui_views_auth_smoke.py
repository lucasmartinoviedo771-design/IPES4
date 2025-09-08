# tests/test_ui_views_auth_smoke.py
import pytest
from django.contrib.auth import get_user_model
from django.urls import URLPattern, URLResolver, get_resolver, reverse, NoReverseMatch

SAFE = {200, 301, 302, 403, 404, 405}


def _available_names() -> set[str]:
    # Sólo nombres de URL (excluye callables)
    return {k for k in get_resolver().reverse_dict.keys() if isinstance(k, str)}


@pytest.mark.django_db
def test_panel_dashboard_auth_smoke(client):
    User = get_user_model()
    User.objects.create_user(
        username="smoke", password="pass12345", is_staff=True, is_superuser=True
    )
    client.login(username="smoke", password="pass12345")

    candidates = {"panel_dashboard", "ui:dashboard", "dashboard"}
    available = _available_names()
    found = next((n for n in candidates if n in available), None)
    if not found:
        pytest.skip("No se encontró una vista de dashboard nombrada")
    url = "/"                      # valor seguro por defecto
    try:
        url = reverse(found)
    except NoReverseMatch:
        pytest.skip("NoReverseMatch para la vista de dashboard")

    resp = client.get(url, follow=False)
    assert resp.status_code in {200, 302, 403}