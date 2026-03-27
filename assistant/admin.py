from django.contrib import admin
from .models import Farmer, CallSession, QueryLog

admin.site.register(Farmer)
admin.site.register(CallSession)
admin.site.register(QueryLog)