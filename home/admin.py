from django.contrib import admin


from .models import PatientProfile, Departments, Doctors, Booking

admin.site.register(Departments)
admin.site.register(Doctors)


class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'image', 'address', 'country', 'state', 'blood_grp')
    search_fields = ('patient_name', 'doctor_name__doc_name')


admin.site.register(PatientProfile, PatientProfileAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_name', 'patient_phone', 'patient_email', 'doctor_name', 'booking_date', 'booked_on')


admin.site.register(Booking, BookingAdmin)
