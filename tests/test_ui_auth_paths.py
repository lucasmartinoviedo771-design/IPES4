import pytest
from django.contrib.auth import get_user_model

SAFE = {200, 301, 302, 403, 404}

CANDIDATES = [
    "/ui/",
    "/ui/estudiantes/list/",
    "/ui/docentes/list/",
    "/ui/dashboard/",
]

@pytest.mark.django_db
def test_ui_paths_authenticated(client):
    User = get_user_model()
    _ = User.objects.create_user(username="tester", password="pass12345", is_staff=True)
    client.login(username="tester", password="pass12345")

    for url in CANDIDATES:
        resp = client.get(url, follow=False)
        assert resp.status_code in SAFE, f"{url} -> {resp.status_code}"
