from django import forms
from tinymce.widgets import TinyMCE
from django.contrib import admin
from .models import Presentation, Slide, Participant, Score
from .models import Branding

@admin.register(Branding)
class BrandingAdmin(admin.ModelAdmin):
    list_display = ("site_name",)


# --------- TinyMCE form for slides ---------
class SlideForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            mce_attrs={
                "height": 400,
                "menubar": True,
                "plugins": (
                    "advlist autolink lists link image charmap preview anchor "
                    "searchreplace visualblocks code fullscreen "
                    "insertdatetime media table paste code help wordcount"
                ),
                "toolbar": (
                    "undo redo | formatselect | "
                    "bold italic underline forecolor backcolor | "
                    "alignleft aligncenter alignright alignjustify | "
                    "bullist numlist outdent indent | removeformat | "
                    "table link image | code fullscreen"
                ),
                "branding": False,
            }
        )
    )

    # make code_snippet look like a code editor (monospace, bigger)
    code_snippet = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "style": "font-family: monospace; background:#1e1e1e; color:#dcdcdc;"
                         "border-radius:6px; padding:10px; width:95%;"
            }
        ),
        label="Code Snippet",
    )

    class Meta:
        model = Slide
        fields = "__all__"


# --------- Inline for slides (stacked view for clean layout) ---------
class SlideInline(admin.StackedInline):
    model = Slide
    form = SlideForm
    extra = 1
    fields = ("title", "content", "code_snippet", "slide_order")
    ordering = ("slide_order",)
    show_change_link = True   # optional: adds "Edit" button for slides
    classes = ["collapse"]    # optional: collapsible slide sections


class PresentationAdmin(admin.ModelAdmin):
    list_display = ("topic", "name", "created_on", "slide_count")
    search_fields = ("topic", "name")
    list_filter = ("created_on",)
    ordering = ("-created_on",)
    inlines = [SlideInline]

    def slide_count(self, obj):
        return obj.slides.count()
    slide_count.short_description = "Slides"

    class Media:
        js = ("js/mode_contrast.js",)   # JavaScript
        css = {"all": ("css/mode_contrast.css",)}  # Dark mode styles


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
