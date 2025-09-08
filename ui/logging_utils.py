# ui/logging_utils.py
from django.http import QueryDict

SAFE_LOG_KEYS = {"plan_id", "materia_id", "docente_id", "profesorado_id"}


def sanitize_params(qd: QueryDict) -> dict:
    try:
        return {k: qd.get(k) for k in qd.keys() if k in SAFE_LOG_KEYS}
    except Exception:
        return {}
