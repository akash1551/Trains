from django.contrib import admin
admin.autodiscover()
from irctc.models import UserDetail,Train,Reservation,Station,Location
# Register your models here.

admin.site.register(UserDetail)
admin.site.register(Train)
admin.site.register(Reservation)
admin.site.register(Station)
admin.site.register(Location)