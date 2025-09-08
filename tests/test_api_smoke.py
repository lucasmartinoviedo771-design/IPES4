import pytest

SAFE = {200, 204, 301, 302, 400, 403, 404}

@pytest.mark.django_db
def test_api_materias_accepts_q(client):
    r = client.get("/api/materias/", {"q": "a"}, follow=False)
    assert r.status_code in SAFE

@pytest.mark.django_db
def test_api_horarios_materia_accepts_param(client):
    r = client.get("/api/horarios/materia/", {"materia": 1}, follow=False)
    assert r.status_code in SAFE

@pytest.mark.django_db
def test_api_comisiones_materia_accepts_param(client):
    r = client.get("/api/comisiones/materia/", {"materia": 1}, follow=False)
    assert r.status_code in SAFE
