from datetime import time

import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_timeslot_valid_window():
    ts = baker.make(
        "academia_horarios.TimeSlot",
        dia_semana=1,             # lunes (ajusta si tu modelo usa otro rango)
        inicio=time(8, 0, 0),
        fin=time(9, 0, 0),
        turno="manana",           # ajusta si tus choices usan otros valores
    )
    assert ts.pk
