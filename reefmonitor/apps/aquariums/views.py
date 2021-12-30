from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Aquarium

# Create your views here.
@login_required(login_url="/login/")
def home_view(request):
    user = request.user

    aquariums = Aquarium.objects.filter(owner=user)
    
    context = {"aquariums": aquariums}
    return render(request, "dashboard/home.html", context)