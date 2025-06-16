from django.contrib import admin
from .models import Person, Project, Technology, Skill, ProjectImage

# Register your models here.
admin.site.register(Person)
admin.site.register(Project)
admin.site.register(Technology)
admin.site.register(Skill)
admin.site.register(ProjectImage)
