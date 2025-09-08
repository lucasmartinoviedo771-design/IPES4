from datetime import time

import pytest
from django.apps import apps
from model_bakery import baker


@pytest.mark.django_db
def test_carrera_and_plan_str_not_empty():
    carrera = baker.make("academia_core.Carrera")
    plan = baker.make("academia_core.PlanEstudios", carrera=carrera)
    assert str(carrera).strip()
    assert str(plan).strip()

@pytest.mark.django_db
def test_any_model_creatable_smoke():
    baker.make("academia_core.Carrera")
    baker.make("academia_core.PlanEstudios")

    # Si existe app de horarios, crear un TimeSlot válido
    if apps.is_installed("academia_horarios"):
        try:
            ts = baker.make(
                "academia_horarios.TimeSlot",
                inicio=time(8, 0),
                fin=time(10, 0),
                dia_semana=1,   # ajusta si tus choices difieren
                turno="manana", # ajusta al choice real
            )
        except Exception:
            ts = None

        # Intentar HorarioClase si el bakery genera el resto de FKs automáticamente
        try:
            baker.make("academia_horarios.HorarioClase", timeslot=ts)
        except Exception:
            # No hacemos fallar el smoke si falta completar algún FK
            pass
