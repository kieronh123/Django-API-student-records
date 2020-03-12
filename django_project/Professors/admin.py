from django.contrib import admin
from .models import *

class ModulesAdmin(admin.ModelAdmin):
#    list_display = ('moduleID',)
#    search_fields = ('moduleID',)
    filter_horizontal = ('moduleProfessors',)


admin.site.register(ModulesTaughtBy, ModulesAdmin)
admin.site.register(Professors)
admin.site.register(ProfessorTitle)
admin.site.register(ModuleCode)
admin.site.register(ModuleName)
admin.site.register(ModuleYearSemester)
admin.site.register(RateProfessor)

