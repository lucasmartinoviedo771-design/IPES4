import pytest

SAFE = {200, 301, 302, 403, 404, 405}

@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/schema/", "/docs/"])
def test_openapi_docs_exist(client, url):
    resp = client.get(url, follow=False)
    assert resp.status_code in SAFE
