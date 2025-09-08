from django.http import QueryDict

from ui.logging_utils import sanitize_params


def test_sanitize_params_filters_unknown_keys():
    qd = QueryDict("plan_id=1&x=999&materia_id=3&foo=bar")
    out = sanitize_params(qd)
    assert out == {"plan_id": "1", "materia_id": "3"}


def test_sanitize_params_handles_broken_querydict(monkeypatch):
    class BrokenQD(QueryDict):
        def keys(self):
            raise RuntimeError("boom")

    out = sanitize_params(BrokenQD(""))
    assert out == {}
