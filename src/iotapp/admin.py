from django.contrib import admin
from .models import Device, FavouriteDevice, Profile, Snap, TagDict

# Register your models here.
admin.site.register(Device)
admin.site.register(FavouriteDevice)
admin.site.register(Profile)
admin.site.register(Snap)
admin.site.register(TagDict)