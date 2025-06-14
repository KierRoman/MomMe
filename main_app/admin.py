from django.contrib import admin
from .models import Baby, Feeding, Diaper, Appointment, Medicine, UserProfile

# Register your models here.
admin.site.register(Baby)
admin.site.register(Feeding)
admin.site.register(Diaper)
admin.site.register(Appointment)
admin.site.register(Medicine)