import os, json

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

from .models import UserPreference


# Create your views here.

def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, "currencies.json")

    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        for abbr, full_name in data.items():
            currency_data.append({"full_name": full_name, "abbr": abbr})

    user_preferences, is_created = UserPreference.objects.get_or_create(user=request.user)
    context = {"currencies": currency_data, "user_preferences": user_preferences}

    if request.method == "GET":
      return render(request, "preferences/index.html", context)

    else:  # POST method
        currency = request.POST["currency"]
        user_preferences.currency = currency
        user_preferences.save()
        messages.success(request, "Changes saved")

        return render(request, "preferences/index.html", context)
