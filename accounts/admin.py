from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register your models here.

admin.site.register(Profile)


# Path: accounts/admin.py
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_consumer",
        "whichapp",
        "is_employee",
        "is_terms",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_consumer",
        "whichapp",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_consumer",
                    "whichapp",
                    "is_employee",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
