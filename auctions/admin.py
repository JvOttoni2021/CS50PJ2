from django.contrib import admin

from . import models

admin.site.register(models.Listing)
admin.site.register(models.Category)
admin.site.register(models.Bid)
admin.site.register(models.User)
admin.site.register(models.WatchList)
admin.site.register(models.Comment)