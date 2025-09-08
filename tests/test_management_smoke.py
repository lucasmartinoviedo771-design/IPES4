import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_django_check_runs_without_exception():
    # No aserción: si hay excepción, falla el test.
    call_command("check")

@pytest.mark.django_db
def test_showmigrations_plan_runs():
    # Solo valida que ejecute sin explotar.
    call_command("showmigrations", "--plan")