from django.contrib import admin

from user.models import User, Job, Company

# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Company)
