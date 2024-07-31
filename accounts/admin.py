from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail

from .models import CustomUser


@admin.action(description='Approve selected doctors')
def approve_doctors(modeladmin, request, queryset):
    doctors = queryset.filter(is_doctor=True)
    doctors.update(is_approved=True)

    for doctor in doctors:
        send_mail(
            'Registration Approved',
            'Dear {},\n\nYour registration has been approved by the admin.\n\nBest regards,'
            '\nHospital Management Team'.format(doctor.username), settings.DEFAULT_FROM_EMAIL,
            [doctor.email], fail_silently=False,)


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
