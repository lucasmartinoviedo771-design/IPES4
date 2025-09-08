import re

import pytest
from django.urls import URLPattern, URLResolver, get_resolver

SAFE_STATUS = {200, 301, 302, 400, 403, 404, 405}
EXCLUDE_PREFIXES = (
    "admin",  # admin
    "__debug__",  # toolbar
    "_nested_admin",  # si estuviera
    "static",  # servido por whitenoise/nginx
    "media",  # idem
)


def iter_patterns(patterns, base=""):
    for p in patterns:
        if isinstance(p, URLResolver):
            yield from iter_patterns(p.url_patterns, base + str(p.pattern))
        elif isinstance(p, URLPattern):
            full = (base + str(p.pattern)).lstrip("^").lstrip("/")
            yield (full, p)


def is_argless(pattern: URLPattern) -> bool:
    # Acepta solo rutas sin converters (path('<id>/'...) → no)
    pat = pattern.pattern
    # Django 5: RoutePattern.converters o RegexPattern.regex
    if hasattr(pat, "converters"):
        return not bool(pat.converters)
    if hasattr(pat, "regex"):
        return pat.regex.groups == 0
    # fallback conservador
    s = str(pat)
    return ("<" not in s) and (re.search(r"\(.+?\)", s) is None)


def collect_simple_urls():
    resolver = get_resolver()
    urls = []
    for url_str, patt in iter_patterns(resolver.url_patterns):
        if not url_str:
            continue
        if any(url_str.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            continue
        if is_argless(patt):
            # normaliza terminación
            if not url_str.endswith("/"):
                url_str += "/"
            urls.append("/" + url_str)
    # quita duplicados manteniendo orden
    seen = set()
    dedup = []
    for u in urls:
        if u not in seen:
            dedup.append(u)
            seen.add(u)
    return dedup


SMOKE_URLS = collect_simple_urls()


@pytest.mark.parametrize("url", SMOKE_URLS or ["/"])  # si no encuentra ninguna, prueba home "/"
@pytest.mark.django_db
def test_simple_urls_dont_500(client, url):
    resp = client.get(url, follow=False)
    assert resp.status_code in SAFE_STATUS, f"{url} -> {resp.status_code}"
