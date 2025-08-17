from django.shortcuts import render, redirect, get_object_or_404
from .models import Image


def image (request):
    image = Image.objects.all()
    return render(request, 'slide_profile/slide_image_list.html', {"images":image})


def delete_image(request, pk):
    image = get_object_or_404(Image, id=pk)
    image.delete()
    return redirect('image')

def add_image(request):
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
            return redirect('image')
        else:
            error = "Title and Image are required."
            return render(request, 'slide_profile/add_image_manual.html', {'error': error})
    
    return render(request, 'slide_profile/add_image_manual.html')
