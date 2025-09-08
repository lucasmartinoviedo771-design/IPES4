# tests/test_api_params_smoke.py
import pytest
from django.contrib.auth import get_user_model

SAFE = {200, 301, 302, 400, 403, 404, 405}

CASES = [
    ("/api/materias/", {"plan_id": 1}),
    ("/api/horarios/materia/", {"materia_id": 1}),
    ("/api/comisiones/materia/", {"materia_id": 1}),
    pytest.param(
        "/api/horarios/docente",
        {"docente_id": 1},
        marks=pytest.mark.xfail(reason="endpoint con bug conocido en views_api (valores/campos)"),
    ),
    pytest.param(
        "/api/horarios/profesorado",
        {"profesorado_id": 1},
        marks=pytest.mark.xfail(reason="endpoint con bug conocido en views_api (valores/campos)"),
    ),
    ("/api/horarios/materia-plan", {"materia_id": 1, "plan_id": 1}),
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url,params",
    [
        ("/panel/horarios/api/materias/", {"plan_id": 1}),
        ("/panel/horarios/api/planes/", {"carrera_id": 1}),
    ],
)
def test_api_with_params_auth(client, url, params):
    User = get_user_model()
    _ = User.objects.create_user(
        username="smoke", password="pass12345", is_staff=True, is_superuser=True
    )
    client.login(username="smoke", password="pass12345")
    resp = client.get(url, params, follow=False)
    assert resp.status_code in SAFE, f"{url} -> {resp.status_code}"
