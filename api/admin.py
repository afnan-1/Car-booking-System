from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(UserProfile)
admin.site.register(Booking)
admin.site.register(Cars)
admin.site.register(Reviews)
