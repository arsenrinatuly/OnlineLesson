from django.shortcuts import render
from django.core.paginator import Paginator




def index(request):
    return render(request, 'idk/index.html')
