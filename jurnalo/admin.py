from django.contrib import admin
from jurnalo.models import Entity, Record


class EntityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Entity, EntityAdmin)


class RecordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Record, RecordAdmin)

