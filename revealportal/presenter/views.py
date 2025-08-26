from django.shortcuts import render, get_object_or_404
from .models import Presentation


def home(request):
    presentations = Presentation.objects.all()
    return render(request, 'home.html', {'presentations': presentations})

def presentation_view(request, id):
    presentation = get_object_or_404(Presentation, id=id)
    slides = presentation.slide_set.order_by('slide_order')
    return render(request, 'presentation.html', {
        'presentation': presentation,
        'slides': slides
    })


def impress_presentation_view(request, id):
    presentation = get_object_or_404(Presentation, id=id)
    slides = presentation.slide_set.order_by('slide_order')

    # Generate positions for each slide
    slide_data = []
    spacing = 1000
    for i, slide in enumerate(slides):
        slide_data.append({
            'title': slide.title,
            'content': slide.content,
            'x': i * spacing,
            'y': i * spacing,
        })

    return render(request, 'impress_presentation.html', {
        'presentation': presentation,
        'slides': slide_data
    })