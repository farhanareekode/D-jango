from django.contrib import admin


from .models import PatientProfile, Departments, Doctors, Booking, DoctorsProfile

admin.site.register(Departments)
admin.site.register(Doctors)
admin.site.register(DoctorsProfile)


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'image', 'address', 'country', 'state', 'blood_grp')
    search_fields = ('patient_name', 'doctor_name__doc_name')


admin.site.register(PatientProfile, PatientProfileAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'patient_name', 'patient_phone', 'patient_email', 'doctor_name',
                    'booking_date', 'booked_on', 'user_email', 'is_approved')
    actions = ['approve_bookings']

    def approve_bookings(self, request, queryset):
        queryset.update(is_approved=True)

    approve_bookings.short_description = "Approve selected bookings"

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    search_fields = ('patient_name', 'doctor_name__name', 'user__username')


admin.site.register(Booking, BookingAdmin)

