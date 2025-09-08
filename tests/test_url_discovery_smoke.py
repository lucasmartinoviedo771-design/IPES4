import pytest
from django.contrib.auth import get_user_model
from django.urls import URLPattern, URLResolver, get_resolver

SAFE = {200, 301, 302, 400, 403, 404, 405}


def _flatten(resolver, prefix=""):
    """Devuelve rutas (strings) sin parámetros, juntando prefijos."""
    for entry in resolver.url_patterns:
        if isinstance(entry, URLPattern):
            route = f"{prefix}{entry.pattern}"
            route = str(route)
            # saltamos rutas con parámetros (<id>, etc.)
            if "<" in route or ">" in route:
                continue
            # normalizamos barra inicial
            if not route.startswith("/"):
                route = "/" + route
            yield route
        elif isinstance(entry, URLResolver):
            new_prefix = f"{prefix}{entry.pattern}"
            yield from _flatten(entry, prefix=str(new_prefix))


def _unique_cleaned_routes():
    # Partimos del urls raíz del proyecto
    resolver = get_resolver()
    seen = set()
    for r in _flatten(resolver):
        # quitamos dobles barras y rutas obvias a excluir si molestan
        r = r.replace("//", "/")
        if r not in seen:
            seen.add(r)
            yield r


ALL_ROUTES = list(_unique_cleaned_routes())


@pytest.mark.parametrize("route", ALL_ROUTES or ["/"])
@pytest.mark.django_db
def test_routes_no_500_anonymous(client, route):
    resp = client.get(route, follow=False)
    assert resp.status_code in SAFE, f"{route} -> {resp.status_code}"


@pytest.mark.parametrize("route", ALL_ROUTES[:80] or ["/"])  # límite para no alargar mucho
@pytest.mark.django_db
def test_routes_no_500_authenticated(client, route):
    User = get_user_model()
    _ = User.objects.create_user(
        username="smoke", password="pass12345", is_staff=True, is_superuser=True
    )
    client.login(username="smoke", password="pass12345")
    resp = client.get(route, follow=False)
    assert resp.status_code in SAFE, f"(auth){route} -> {resp.status_code}"
