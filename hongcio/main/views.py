from django.shortcuts import render

# Create your views here.
def test(request):
    return render(request, 'main/index_rework.html')


def index(request):
    return render(request, 'main/index.html')