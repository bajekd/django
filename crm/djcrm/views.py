from django.shortcuts import render, reverse
from django.views import generic

from .forms import ArenaForm

# Create your views here.

def ArenaCreateView(generic.CreateView):
  template_name = "arena/arena_create.html"

'''
def arena_create(request):
  form = ArenaForm()
  if request.method == "POST":
    form = ArenaForm(request.POST)
'''

  
