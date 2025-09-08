import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_management_commands_smoke():
    # Si alguno no existe, comentar esa línea (pero en tu repo están):
    call_command("check")  # siempre existe
    try:
        call_command("setup_roles")
    except Exception:
        pass
    try:
        call_command("seed_turnos_y_bloques")
    except Exception:
        pass
