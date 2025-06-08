from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to display in the user list view
    list_display = ("username", "email", "job_role", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Add job_role field to existing fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("job_role",)}),
    )

    # Add job_role field when creating new users in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("job_role",)}),
    )

    search_fields = ("email", "username")
    ordering = ("email",)
