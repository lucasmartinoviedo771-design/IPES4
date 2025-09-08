import pytest

SAFE = {200, 301, 302, 400, 403, 404, 405}


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url,params",
    [
        ("/api/materias/", {"plan_id": 1}),
        ("/api/horarios/materia/", {"materia_id": 1}),
        ("/api/comisiones/materia/", {"materia_id": 1}),
        ("/api/horarios/docente", {"docente_id": 1}),
        ("/api/horarios/profesorado", {"profesorado_id": 1}),
        ("/api/horarios/materia-plan", {"materia_id": 1, "plan_id": 1}),
    ],
)
def test_api_with_params_no_500(client, url, params):
    """Con los parámetros mínimos, la API no debe devolver 500."""
    resp = client.get(url, params, follow=False)
    assert resp.status_code in SAFE, f"{url} -> {resp.status_code} ({resp.content[:200]!r})"
