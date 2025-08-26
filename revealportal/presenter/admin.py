# presenter/admin.py
from django.contrib import admin
from .models import Presentation, Slide, Participant, Score


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 1
    fields = ("title", "slide_order", "code_snippet")
    ordering = ("slide_order",)


class PresentationAdmin(admin.ModelAdmin):
    list_display = ("topic", "name", "created_on", "slide_count")
    search_fields = ("topic", "name")
    list_filter = ("created_on",)
    ordering = ("-created_on",)
    inlines = [SlideInline]

    def slide_count(self, obj):
        return obj.slides.count()
    slide_count.short_description = "Slides"


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 0
    readonly_fields = ("presentation", "points", "created_on")
    ordering = ("-created_on",)


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("name", "joined_on", "total_points")
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [ScoreInline]

    def total_points(self, obj):
        return sum(score.points for score in obj.scores.all())
    total_points.short_description = "Total Points"


class ScoreAdmin(admin.ModelAdmin):
    list_display = ("participant", "presentation", "points", "created_on")
    list_filter = ("presentation", "created_on")
    search_fields = ("participant__name", "presentation__topic")
    ordering = ("-created_on",)


admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Score, ScoreAdmin)
