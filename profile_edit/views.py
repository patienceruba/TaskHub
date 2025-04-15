from django.shortcuts import render

# Create your views here.
def profile_edit(request):
    return render(request, "profile_edit/pro_edit.html")


def person(request):
    return render(request, "profile_edit/person.html")