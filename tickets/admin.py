from django.contrib import admin
from .models import Ticket
from django.utils.html import format_html

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'location', 'category', 'priority', 'phone_number', 'submitted_at')
    readonly_fields = ('submitted_at',)
    fields = (
        'image', 'location', 'comments', 'phone_number',
        'summary', 'category', 'priority', 'submitted_at'
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;" />', obj.image.url)
        return "No Image"
    thumbnail.short_description = 'Image'
