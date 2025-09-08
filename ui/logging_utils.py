# ui/logging_utils.py
from collections.abc import Iterable


def safe_params(request, allowed: Iterable[str]) -> dict:
    # Loguea solo claves esperadas y trunca valores para evitar inyección
    return {k: request.GET.get(k, "")[:100] for k in allowed if k in request.GET}
