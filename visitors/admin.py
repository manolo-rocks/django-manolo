from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from visitors.models import Subscriber, Visitor, Developer, Institution


# Define an inline admin descriptor for Subscriber model
# which acts a bit like a singleton
class SubscriberInline(admin.StackedInline):
    model = Subscriber
    can_delete = False
    verbose_name_plural = 'subscribers'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (SubscriberInline, )


class InstitutionAdmin(admin.ModelAdmin):
    model = Institution


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Visitor)
admin.site.register(Developer)
