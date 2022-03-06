from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Aquarium, Parameter
from .forms import AquariumForm, MeasurementForm
from .handler import Handler

from datetime import datetime, timedelta
import json

@login_required(login_url="/login/")
def home_view(request):
    # Initialize form for creating a new aquarium
    form = AquariumForm(request.POST or None)

    # Retrieve user and its aquariums
    user = request.user
    aquariums = Aquarium.objects.filter(owner=user)

    # Try to get the latest values and localize the time for each aquarium
    latest = {}
    for aq in aquariums:
        aq.update_date = timezone.localtime(aq.update_date)

        # Try comm with database, if not available --> no value to display
        try:
            handler = Handler(aq.id)
            latest[aq.id] = handler.GetLatestMeasurements()
        except:
            latest[aq.id] = {}

    msg = None

    # Validate form
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get("name")

            if Aquarium.objects.filter(owner=user, name=name).count() > 0:
                msg = f'There already exists an aquarium with the name: {name}'
            else:    
                form.save(name, user)
                return redirect("/")
        else:
            msg = 'Error validating the form'
         
    
    context = {
        "aquariums": aquariums, 
        "latest": latest,
        "form": form, 
        "msg": msg,
        "query": seven_days_query_param()
    }

    
    context['parameter_units'] = Parameter.Units.choices

    return render(request, "dashboard/home.html", context)


@login_required(login_url="/login/")
def delete_view(request, aquarium_id):
    user = request.user 

    # Check if user has access to this aquarium
    if Aquarium.objects.filter(owner=user, id=aquarium_id).count() == 0:
        return redirect("/")


    handler = Handler(aquarium_id)
    if request.method == "POST":
        handler.Delete()
        return redirect("/")
         
    
    context = {"aquarium": handler.aquarium}
    return render(request, "dashboard/delete.html", context)


@login_required(login_url="/login/")
def overview_view(request, aquarium_id):
    # Create context and attach mapping for parameters
    context = {}
    context['parameter_names'] = Parameter.Name.choices
    context['parameter_units'] = Parameter.Units.choices
    context['parameter_units_json'] = json.dumps(Parameter.Units.choices)

    # Retrieve time range from query params
    time_end = timezone.now()
    time_end_str = request.GET.get('end', None)

    if time_end_str != None:
        time_end = datetime.fromisoformat(time_end_str)

    time_start = datetime.fromisoformat(request.GET.get('start', str(time_end - timedelta(days=7))))
    offset = time_end - time_start
    # If invalid time range given, fall back to last 7 days
    if offset.total_seconds() <= 0:
        time_end = datetime.now()
        time_start = time_end - timedelta(days=7)
    context['time_end'] = time_end
    context['time_start'] = time_start

    # Get current user and corresponding aquariums for nav bar
    user = request.user
    aquariums = Aquarium.objects.filter(owner=user)
    context['aquariums'] = aquariums

    # Attach measurement form
    form = MeasurementForm(request.POST or None)
    context['form'] = form

    # Get currently selected aquarium and open db connection to retrieve measurements from selected time range
    handler = Handler(aquarium_id)
    parameters = handler.GetMeasurements(time_start, time_end)

    # Data for visualizing available parameters
    context['parameters_dict'] = parameters

    # Data for building graphs
    context['parameters'] = json.dumps(parameters)

    # Handle measurement form
    if request.method == "POST":
        if form.is_valid():
            # Retrieve datetime for measurement
            date = request.POST.get('date')
            time = request.POST.get('time')
            datetime_str = date + "T" + time + "Z"
            timestamp = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')

            measurement = form.ToMeasurement(time_to_local(timestamp))
            handler.AddMeasurement(measurement=measurement, external=False)
            measurement.delete()
            context['time_end'] = timezone.now()
        else:
            print("Form not valid")
        return render(request, "dashboard/overview.html", context)

    return render(request, "dashboard/overview.html", context)

def seven_days_query_param():
    end = datetime.now()
    days = timedelta(7)
    start = end - days

    return "?start=" + start.isoformat() + "&end=" + end.isoformat()

def time_to_local(timestamp):
    tz = timezone.get_current_timezone()
    return tz.localize(timestamp)