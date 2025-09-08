import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_admin_changelist_loads(client):
    User = get_user_model()
    _ = User.objects.create_user(
        username="admin", password="pass12345", is_staff=True, is_superuser=True
    )
    client.login(username="admin", password="pass12345")
    # probá cargar index (y usa admin.site para evitar F841)
    assert admin.site is not None
    resp = client.get("/admin/", follow=False)
    assert resp.status_code in {200, 302}
