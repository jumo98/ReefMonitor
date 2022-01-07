from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reefmonitor.apps.notifications.email import EMailHandler

from reefmonitor.apps.rules.forms import RuleForm
from reefmonitor.apps.rules.models import Rule, Violation

from ..aquariums.models import Aquarium, Parameter

@login_required(login_url="/login/")
def rules_view(request, aquarium_id):
    form = RuleForm(request.POST or None)

    context = {
        "form_create": form
    }

    # Retrieve aquariums
    user = request.user
    aquariums = Aquarium.objects.filter(owner=user)
    aquarium = Aquarium.objects.get(id=aquarium_id)

    context["aquariums"] = aquariums
    context["aquarium"] = aquarium

    context["parameters"] = Parameter.Name.choices
    context["types"] = Rule.Type.choices

    id = request.GET.get("id")
    if id:
        selected_rule = Rule.objects.get(id=id)
        context["selected_rule"] = Rule.objects.get(id=id)
        form_edit = RuleForm(request.POST or None)
        form_edit.initial["edit"] = True
        form_edit.initial["value"] = selected_rule.value
        form_edit.initial["parameter"] = selected_rule.parameter
        form_edit.initial["type"] = selected_rule.type
        context["form_edit"] = form_edit

    rules = Rule.objects.filter(aquarium=aquarium).order_by('parameter')
    context["rules"] = rules

    msg = None

    if request.method == "POST":
        if 'delete' in request.POST:
            id = request.POST.get('delete')
            rule = Rule.objects.get(id=id)
            rule.Delete()
            return redirect(f"/{aquarium_id}/rules")
        elif form.is_valid():
            if 'edit' in request.POST:
                form.update(context["selected_rule"].id)
            elif 'create' in request.POST:
                form.save(aquarium)

            return redirect(f"/{aquarium_id}/rules")
        else:
            msg = 'Error validating the form'

    return render(request, "dashboard/rules.html", context)


@login_required(login_url="/login/")
def analyze_view(request, aquarium_id):
    context = {}
    # Retrieve aquariums
    user = request.user
    aquariums = Aquarium.objects.filter(owner=user)
    aquarium = Aquarium.objects.get(id=aquarium_id)

    context["aquariums"] = aquariums
    context["aquarium"] = aquarium

    violations = Violation.objects.filter(aquarium=aquarium).order_by('-timestamp')[:15]
    context["violations"] = violations

    return render(request, "dashboard/analyze.html", context)