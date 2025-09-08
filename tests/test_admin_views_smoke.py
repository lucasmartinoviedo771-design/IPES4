import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

SAFE = {200, 301, 302, 403, 404, 405}

@pytest.mark.django_db
def test_admin_index_authenticated(client):
    User = get_user_model()
    User.objects.create_superuser("smoke_admin", "a @a.com", "pass12345")
    assert client.login(username="smoke_admin", password="pass12345")
    resp = client.get(reverse("admin:index"), follow=False)
    assert resp.status_code in SAFE, f"/admin/ -> {resp.status_code}"

@pytest.mark.django_db
def test_admin_auth_applist_authenticated(client):
    User = get_user_model()
    User.objects.create_superuser("smoke_admin2", "b @b.com", "pass12345")
    assert client.login(username="smoke_admin2", password="pass12345")
    url = reverse("admin:app_list", kwargs={"app_label": "auth"})
    resp = client.get(url, follow=False)
    assert resp.status_code in SAFE, f"{url} -> {resp.status_code}"
