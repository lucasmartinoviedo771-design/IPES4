# tests/test_ui_views_auth_smoke.py
import pytest
from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch, URLPattern, URLResolver, get_resolver, reverse

SAFE = {200, 301, 302, 403, 404, 405}


def _collect_named_urls():
    resolver = get_resolver()
    names = set()

    def walk(patterns):
        for p in patterns:
            if isinstance(p, URLPattern):
                if p.name:
                    names.add(p.name)
            elif isinstance(p, URLResolver):
                walk(p.url_patterns)

    walk(resolver.url_patterns)
    return names


@pytest.mark.django_db
def test_panel_dashboard_auth_smoke(client):
    candidates = {"panel_dashboard", "ui:dashboard", "dashboard"}
    available = _collect_named_urls()
    found = next((n for n in candidates if n in available), None)
    url = "/admin/"  # Default value

    if not found:
        pytest.skip("No se encontró una vista de dashboard nombrada")

    try:
        url = reverse(found)
    except NoReverseMatch:
        if ":" not in found:
            try:
                url = reverse(f"ui:{found}")
            except NoReverseMatch:
                pytest.skip(f"Reverse no disponible para {found}")
        else:
            pytest.skip(f"Reverse no disponible para {found}")

    User = get_user_model()
    User.objects.create_user(
        username="smoke", password="pass12345", is_staff=True, is_superuser=True
    )
    client.login(username="smoke", password="pass12345")
    resp = client.get(url, follow=False)
    assert resp.status_code in SAFE
