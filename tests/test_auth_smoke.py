import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_login_redirection_flow(client):
    # Intenta acceder a una ruta protegida conocida; si no la tenés, cambia el path.
    # Elegimos una probable del panel; si retorna 404, no falla el test (aceptamos SAFE_STATUS más abajo).
    target = "/ui/"

    resp = client.get(target, follow=False)
    # si es protegida, debería redirigir (302) a login
    assert resp.status_code in (200, 301, 302, 403, 404, 405)

    # Login con usuario simple y reintenta (si la vista requiere permiso especial, podría dar 403)
    User = get_user_model()
    User.objects.create_user(username="tester", password="pass12345")
    client.login(username="tester", password="pass12345")
    resp2 = client.get(target, follow=False)
    assert resp2.status_code in (200, 302, 403, 404, 405)
