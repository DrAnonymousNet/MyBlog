from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.unregister(User)

@admin.register(User)
class CustomUerAdmin(UserAdmin):
    readonly_fields = [
                        "date_joined",
                        "last_login"

                       ]
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        disabled_form = set()

        if not request.user.is_superuser:
            disabled_form |= {
                "is_superuser",
                'user_permissions',
                "username",
                "groups",
                "is_staff"
            }
        print(form.base_fields, type(obj))
        for d in disabled_form:

            form.base_fields[d].disabled = True
        return form
