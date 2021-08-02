from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(UserProfile)
admin.site.register(Booking)
admin.site.register(Cars)
admin.site.register(Reviews)
admin.site.site_header='Car Booking System Admin Panel'
admin.site.index_title='Car Booking System'
admin.site.site_title='Car Booking System Admin Panel'
