from django.contrib import admin
from transcript_analyzer.models import Actor
from transcript_analyzer.models import Character
from transcript_analyzer.models import Episode

# Register your models here.
admin.site.register(Actor)
admin.site.register(Character)
admin.site.register(Episode)
