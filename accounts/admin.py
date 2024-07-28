from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.action(description='Approve selected doctors')
def approve_doctors(modeladmin, request, queryset):
    queryset.filter(is_doctor=True).update(is_approved=True)


class CustomUserAdmin(UserAdmin):
    actions = [approve_doctors]
    list_display = ['username', 'email', 'is_doctor', 'is_approved']
    list_filter = ['is_doctor', 'is_approved']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_approved'].disabled = True
        return form


admin.site.register(CustomUser, CustomUserAdmin)
