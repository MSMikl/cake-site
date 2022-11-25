from django.contrib import admin

from utm.models import UtmCheckin


@admin.register(UtmCheckin)
class UtmCheckinAdmin(admin.ModelAdmin):

    list_display = ('utm_source', 'check_in_date', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term')

    fields = ('utm_source', 'check_in_date', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term')

    readonly_fields = ('utm_source', 'check_in_date', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term')
