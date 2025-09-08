def test_admin_login_page(client):
    resp = client.get("/admin/login/", follow=False)
    assert resp.status_code in {200, 302}
