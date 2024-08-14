from django.contrib import admin
from .models import Transactions
# Register your models here.


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_username', 'booking_id', 'payment_id', 'amount', 'payment_status', 'payment_date',
                    'time_stamp')
    search_fields = ('booking_id', 'doctor_name__doc_name')


admin.site.register(Transactions, TransactionsAdmin)