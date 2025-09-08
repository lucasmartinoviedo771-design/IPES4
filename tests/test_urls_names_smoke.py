import pytest
from django.urls import get_resolver, reverse

SAFE = {200, 301, 302, 403, 404, 405}


def _names_no_args():
    # toma nombres sin argumentos posicionales conocidos
    for name, patterns in get_resolver().reverse_dict.items():
        if not isinstance(name, str):
            continue
        # heurística: si alguna variante no requiere args, probamos
        if any(not params for (route, params) in patterns[0]):
            yield name


@pytest.mark.django_db
@pytest.mark.parametrize("name", list(_names_no_args())[:80])
def test_named_routes_no_500(client, name):
    url = reverse(name)
    resp = client.get(url, follow=False)
    assert resp.status_code in SAFE, f"{name} -> {resp.status_code}"
