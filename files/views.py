from django.shortcuts import render, redirect
from .models import File

def upload_task(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('filedoc')
        if uploaded_file:
            File.objects.create(filedoc=uploaded_file)
            return redirect('files') 

    return render(request, "files/uploadfile.html")
