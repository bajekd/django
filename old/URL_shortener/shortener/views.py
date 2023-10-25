from django.views import View
from django.http import HttpResponseRedirect
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages


from .models import ShortenerURL
from .forms import SubmitURLForm

# Create your views here.
'''
def shortener_fb_view(request, short_code=None, *args, **kwargs):  # function based view
    get_object_or_404(ShortenerURL, short_code=short_code)
    return HttpResponseRedirect("Hello from function {sc}".format(sc=short_code))
'''


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = SubmitURLForm()
        context = {
            "title": "Shorten your URL",
            "form": form,
            "ShortenerURLs": ShortenerURL.objects.all(),
        }
        return render(request, 'shortener/home.html', context)

    def post(self, request, *args, **kwargs):
        form = SubmitURLForm(request.POST)
        context = {
            "title": "Short your URL",
            "form": form,
        }
        if form.is_valid():
            new_url = form.cleaned_data.get('url')
            obj = ShortenerURL.objects.create(url=new_url)
            context = {
                "object": obj,
            }
        else:
            messages.error(request, 'Given url adress is invalid!')
            return redirect('shortener-home')
        return render(request, 'shortener/success.html', context)


class URLRedirectView(View):
    def get(self, request, short_code=None, *args, **kwargs):
        qs = ShortenerURL.objects.filter(short_code=short_code)
        if not qs.exists():
            return render(request, 'shortener/failed.html')
        obj = qs.first()
        obj.count += 1
        obj.save()
        return HttpResponseRedirect(obj.url)
