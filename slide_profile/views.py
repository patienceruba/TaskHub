from django.shortcuts import render, redirect
from .models import Image

def image(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')

        if title and image_file:
            Image.objects.create(
                title=title,
                image=image_file,
                description=description
            )
            return redirect('image_success')
        else:
            error = "Title and Image are required."
            return render(request, 'add_image_manual.html', {'error': error})
    
    return render(request, 'add_image_manual.html')
