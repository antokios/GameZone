from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Developer)
admin.site.register(Game_Review)
admin.site.register(Video)