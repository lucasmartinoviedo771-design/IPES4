from __future__ import annotations

import json
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms_admin import EstudianteCreateForm
from .forms_carga import CargaNotaForm
from .forms_correlativas import CorrelatividadForm
from .models import (
    Carrera,
    Correlatividad,
    EspacioCurricular,
    Estudiante,
    EstudianteProfesorado,
    InscripcionEspacio,
)


@login_required
def home_router(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect("panel")
    perfil = getattr(request.user, "perfil", None)
    if perfil and perfil.rol == "ESTUDIANTE" and perfil.estudiante:
        return redirect("alumno_home")
    return redirect("login")


@login_required
def panel(request: HttpRequest, **kwargs) -> HttpResponse:
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("login")

    action = request.GET.get("action", "section_home")
    ctx = {"action": action, "can_admin": request.user.is_superuser}

    if action == "section_home":
        ctx.update(
            {
                "total_estudiantes": Estudiante.objects.count(),
                "total_profesorados": Carrera.objects.count(),
                "total_espacios": EspacioCurricular.objects.count(),
                "total_inscripciones_carrera": EstudianteProfesorado.objects.count(),
                "total_inscripciones_materia": InscripcionEspacio.objects.count(),
            }
        )
    elif action == "add_est":
        if request.method == "POST":
            form = EstudianteCreateForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Estudiante creado con éxito.")
                return redirect("panel?action=section_est")
        else:
            form = EstudianteCreateForm()
        ctx["form"] = form
    elif action == "section_correlatividades":
        profesorado_id = request.GET.get("profesorado")
        plan_id = request.GET.get("plan")
        materia_principal_id = request.GET.get("materia_principal")

        initial_data = {}
        if profesorado_id:
            initial_data["profesorado"] = profesorado_id
        if plan_id:
            initial_data["plan"] = plan_id
        if materia_principal_id:
            initial_data["materia_principal"] = materia_principal_id

            # Load existing correlatividades for this materia_principal
            existing_correlatividades_regulares = Correlatividad.objects.filter(
                plan_id=plan_id,
                espacio_id=materia_principal_id,
                requisito="REGULARIZADA",
            ).values_list("requiere_espacio", flat=True)

            existing_correlatividades_aprobadas = Correlatividad.objects.filter(
                plan_id=plan_id, espacio_id=materia_principal_id, requisito="APROBADA"
            ).values_list("requiere_espacio", flat=True)

            initial_data["correlativas_regulares"] = list(existing_correlatividades_regulares)
            initial_data["correlativas_aprobadas"] = list(existing_correlatividades_aprobadas)

        if request.method == "POST":
            form = CorrelatividadForm(request.POST, initial=initial_data)
            if form.is_valid():
                form.save()
                messages.success(request, "Correlatividades guardadas con éxito.")
                # Redirect to maintain state
                redirect_url = "/panel/?action=section_correlatividades"
                if form.cleaned_data.get("profesorado"):
                    redirect_url += f"&profesorado={form.cleaned_data['profesorado'].id}"
                if form.cleaned_data.get("plan"):
                    redirect_url += f"&plan={form.cleaned_data['plan'].id}"
                if form.cleaned_data.get("materia_principal"):
                    redirect_url += (
                        f"&materia_principal={form.cleaned_data['materia_principal'].id}"
                    )
                return redirect(redirect_url)
        else:
            form = CorrelatividadForm(initial=initial_data)

        ctx["form"] = form

    elif action in ("insc_carrera", "insc_prof"):
        ctx.update(
            {
                "estudiantes": Estudiante.objects.filter(activo=True).order_by(
                    "apellido", "nombre"
                ),
                "profesorados": Carrera.objects.all().order_by("nombre"),
                "planes_map": json.dumps(
                    {
                        p.id: [{"id": plan.id, "label": plan.resolucion} for plan in p.planes.all()]
                        for p in Carrera.objects.prefetch_related("planes")
                    }
                ),
                "base_checks": [
                    ("doc_dni_legalizado", "DNI legalizado"),
                    ("doc_cert_medico", "Certificado médico"),
                    ("doc_fotos_carnet", "Fotos carnet"),
                    ("doc_folios_oficio", "Folios oficio"),
                ],
                "cohortes": list(range(date.today().year + 1, 2010, -1)),
            }
        )

    return render(request, "academia_core/panel_admin.html", ctx)


@login_required
def panel_correlatividades(request):
    return render(request, "academia_core/panel_correlatividades.html", {})


@login_required
def panel_horarios(request):
    return render(request, "academia_core/panel_horarios.html", {})


@login_required
def panel_docente(request):
    return render(request, "academia_core/panel_docente.html", {})


@login_required
def cargar_nota(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CargaNotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nota guardada con éxito.")
            return redirect("cargar_nota")
    else:
        form = CargaNotaForm()
    return render(request, "academia_core/cargar_nota.html", {"form": form})


@require_POST
def crear_inscripcion_cursada(request, insc_prof_id: int):
    return JsonResponse({"ok": False, "error": "No implementado"}, status=501)


@require_POST
def crear_movimiento(request, insc_cursada_id: int):
    return JsonResponse({"ok": False, "error": "No implementado"}, status=501)


def redir_estudiante(request, dni: str):
    return redirect(f"/panel/?action=section_est&dni={dni}")


def redir_inscripcion(request, insc_id: int):
    return redirect(f"/panel/estudiante/{insc_id}/")


@login_required
def correlatividades_form_view(request):
    if request.method == "POST":
        form = CorrelatividadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("correlatividades_form")
    else:
        form = CorrelatividadForm()
    return render(request, "academia_core/panel_correlatividades_form.html", {"form": form})
