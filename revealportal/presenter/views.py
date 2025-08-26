# presenter/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import json

from .models import Presentation, Participant, Score

# =======================
# Standard Presentation Views
# =======================

def home(request):
    """Homepage: list all presentations"""
    presentations = Presentation.objects.all()
    return render(request, 'home.html', {'presentations': presentations})


def presentation_view(request, id):
    presentation = get_object_or_404(Presentation, id=id)
    slides = presentation.slides.order_by("slide_order")
    return render(request, "presentation.html", {
        "presentation": presentation,
        "slides": slides,
    })


def impress_presentation_view(request, id):
    """Impress.js style 3D presentation view"""
    presentation = get_object_or_404(Presentation, id=id)
    slides = presentation.slides.order_by('slide_order')

    # generate positions for each slide
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


# =======================
# API Endpoints (Gamification)
# =======================

@csrf_exempt
def api_submit_score(request):
    """
    POST JSON: {"name": "Ravi", "points": 10, "presentation": 3}
    Saves score and returns total points.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        name = payload.get('name', 'Guest')[:100]
        points = int(payload.get('points', 0))
        pres_id = payload.get('presentation')
    except Exception as e:
        return JsonResponse({'error': 'invalid payload', 'detail': str(e)}, status=400)

    # ensure participant exists
    participant, _ = Participant.objects.get_or_create(name=name)

    # optional presentation reference
    presentation = None
    if pres_id:
        presentation = Presentation.objects.filter(id=pres_id).first()

    # save score
    Score.objects.create(participant=participant, presentation=presentation, points=points)

    # total points
    total = Score.objects.filter(participant=participant).aggregate(total=Sum('points'))['total'] or 0

    return JsonResponse({'status': 'ok', 'total': total})


def api_leaderboard(request, presentation_id=None):
    """
    Returns leaderboard (aggregated points).
    If presentation_id is provided → filter to that presentation.
    """
    scores = Score.objects.all()
    if presentation_id:
        scores = scores.filter(presentation_id=presentation_id)

    aggregated = scores.values('participant__name').annotate(total=Sum('points')).order_by('-total')[:50]
    data = [{'name': row['participant__name'], 'points': row['total']} for row in aggregated]

    return JsonResponse({'leaderboard': data})
