from django.contrib import admin
from .models import Presentation, Slide

class SlideInline(admin.TabularInline):
    model = Slide
    extra = 1

class PresentationAdmin(admin.ModelAdmin):
    inlines = [SlideInline]

admin.site.register(Presentation, PresentationAdmin)
