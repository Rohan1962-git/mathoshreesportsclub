from django.contrib import admin
from .models import CustomUser, Book_Turf, Admin, Event

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Book_Turf)
admin.site.register(Admin)
admin.site.register(Event)
