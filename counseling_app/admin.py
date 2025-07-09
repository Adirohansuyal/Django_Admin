from django.contrib import admin
from .models import PersonalInfo, MarksEntry, SeatAllotment

admin.site.register(PersonalInfo)
admin.site.register(MarksEntry)
admin.site.register(SeatAllotment)
