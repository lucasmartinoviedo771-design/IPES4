import pytest

SAFE = {200, 301, 302, 403, 404, 405}

@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/schema/", "/docs/"])
def test_docs_pages_do_not_500(client, url):
    resp = client.get(url, follow=False)
    assert resp.status_code in SAFE, f"{url} -> {resp.status_code}"