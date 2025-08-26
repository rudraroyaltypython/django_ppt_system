# context_processors.py
from .models import Branding

def branding_context(request):
    branding = Branding.objects.first()
    return {
        "branding": branding or {"site_name": "Django Presentation System"}
    }
