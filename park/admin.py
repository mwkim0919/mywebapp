from django.contrib import admin

# from forms import *
from park.models import *

class FacilityInline(admin.StackedInline):
	model = Facility
	extra = 1
	# formset = RequiredInlineFormSet

class ParkAdmin(admin.ModelAdmin):
	inlines = [FacilityInline]

admin.site.register(Park, ParkAdmin)
admin.site.register(Facility)
admin.site.register(Last_Updated)

